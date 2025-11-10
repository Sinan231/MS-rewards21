import os
import json
import glob
import logging
from pathlib import Path
from config import Config

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
    handlers=[
        logging.FileHandler(Config.ERROR_LOG_FILE),
        logging.StreamHandler()
    ]
)

def get_edge_profile_paths():
    """
    Detect Microsoft Edge browser profiles on the current system.

    Returns:
        list: List of tuples containing (profile_name, profile_path)
    """
    profiles = []

    # Common Edge profile directories based on OS
    edge_paths = []

    if os.name == 'nt':  # Windows
        # Windows Edge profile paths
        local_app_data = os.environ.get('LOCALAPPDATA', '')
        if local_app_data:
            edge_paths.append(os.path.join(local_app_data, 'Microsoft', 'Edge', 'User Data'))

        # Also check Program Files path
        program_files = os.environ.get('PROGRAMFILES', '')
        if program_files:
            edge_paths.append(os.path.join(program_files, 'Microsoft', 'Edge', 'Application'))

    elif os.name == 'posix':  # macOS and Linux
        home_dir = Path.home()

        # macOS
        if os.path.exists('/Applications/Microsoft Edge.app'):
            edge_paths.append(str(home_dir / 'Library' / 'Application Support' / 'Microsoft Edge'))

        # Linux
        edge_paths.append(str(home_dir / '.config' / 'microsoft-edge'))

    # Search for profiles in detected Edge directories
    for edge_path in edge_paths:
        if os.path.exists(edge_path):
            logging.info(f"Found Edge directory: {edge_path}")

            # Look for profile directories
            profile_pattern = os.path.join(edge_path, 'Profile*')
            profile_dirs = glob.glob(profile_pattern)

            # Also check for "Default Profile" or "Default" directory
            default_paths = [
                os.path.join(edge_path, 'Default'),
                os.path.join(edge_path, 'Default Profile')
            ]

            for default_path in default_paths:
                if os.path.exists(default_path):
                    profile_dirs.append(default_path)

            # Extract profile information
            for profile_dir in profile_dirs:
                if os.path.isdir(profile_dir):
                    profile_name = os.path.basename(profile_dir)

                    # Try to get more friendly profile name from Preferences file
                    preferences_file = os.path.join(profile_dir, 'Preferences')
                    friendly_name = profile_name

                    if os.path.exists(preferences_file):
                        try:
                            with open(preferences_file, 'r', encoding='utf-8') as f:
                                preferences = json.load(f)

                            # Look for profile name in various locations in the JSON
                            name_sources = [
                                preferences.get('profile', {}).get('name'),
                                preferences.get('account_info', [{}])[0].get('full_name'),
                                preferences.get('profile', {}).get('email', ''),
                            ]

                            for name_source in name_sources:
                                if name_source and name_source.strip():
                                    friendly_name = name_source.strip()
                                    break

                        except (json.JSONDecodeError, KeyError, IOError) as e:
                            logging.warning(f"Could not read preferences for {profile_name}: {e}")

                    profiles.append((friendly_name, profile_dir))

    # If no profiles found, provide a default option
    if not profiles:
        logging.warning("No Edge profiles detected, using default profile")
        profiles.append(("Default Profile", "default"))

    return profiles

def select_edge_profile():
    """
    Prompt user to select an Edge browser profile.

    Returns:
        str: Selected profile path or profile identifier
    """
    profiles = get_edge_profile_paths()

    if len(profiles) == 1:
        # Only one profile found, use it automatically
        profile_name, profile_path = profiles[0]
        logging.info(f"Using single detected profile: {profile_name}")
        return profile_path

    print("\n🔍 Detected Microsoft Edge Profiles:")
    print("=" * 60)

    for i, (profile_name, profile_path) in enumerate(profiles, 1):
        # Show a more user-friendly display name
        if profile_name.startswith('Profile'):
            display_name = f"Edge Profile {profile_name.replace('Profile', '')}"
        else:
            display_name = profile_name

        print(f"  {i}. {display_name}")
        print(f"     Path: {profile_path}")
        print()

    print("  0. Use default profile (automatic)")
    print("=" * 60)

    while True:
        try:
            choice = input("Select Edge profile number (0-{}): ".format(len(profiles))).strip()

            if choice == '0':
                logging.info("User selected default profile")
                return "default"

            choice_num = int(choice)
            if 1 <= choice_num <= len(profiles):
                selected_name, selected_path = profiles[choice_num - 1]
                logging.info(f"User selected profile: {selected_name}")
                return selected_path
            else:
                print(f"❌ Please enter a number between 0 and {len(profiles)}")

        except ValueError:
            print("❌ Please enter a valid number")
        except KeyboardInterrupt:
            print("\n❌ Profile selection cancelled")
            return None

def get_profile_user_data_dir(profile_path):
    """
    Convert profile path to the user data directory format needed by Edge.

    Args:
        profile_path (str): Path to the profile directory

    Returns:
        str: User data directory path for Edge WebDriver
    """
    if profile_path == "default":
        # Use the default user data directory
        if os.name == 'nt':  # Windows
            local_app_data = os.environ.get('LOCALAPPDATA', '')
            if local_app_data:
                return os.path.join(local_app_data, 'Microsoft', 'Edge', 'User Data')
        elif os.name == 'posix':  # macOS/Linux
            home_dir = Path.home()
            if os.path.exists('/Applications/Microsoft Edge.app'):  # macOS
                return str(home_dir / 'Library' / 'Application Support' / 'Microsoft Edge')
            else:  # Linux
                return str(home_dir / '.config' / 'microsoft-edge')

    # Extract the base user data directory from the profile path
    # If profile_path is something like /path/to/Edge/User Data/Profile 1
    # we want to return /path/to/Edge/User Data

    # Handle different path formats
    if 'User Data' in profile_path:
        return os.path.dirname(profile_path)
    elif 'microsoft-edge' in profile_path:
        return os.path.dirname(profile_path)
    else:
        # Fallback: assume the profile path is directly usable
        return profile_path

def get_profile_directory_name(profile_path):
    """
    Get the profile directory name from the full profile path.

    Args:
        profile_path (str): Full path to profile directory

    Returns:
        str: Profile directory name (e.g., "Profile 1", "Default")
    """
    if profile_path == "default":
        return "Default"

    return os.path.basename(profile_path)

def test_profile_access(profile_path):
    """
    Test if the selected Edge profile is accessible and valid.

    Args:
        profile_path (str): Path to the Edge profile

    Returns:
        tuple: (success: bool, message: str)
    """
    try:
        if profile_path == "default":
            return True, "Default profile selected"

        if not os.path.exists(profile_path):
            return False, f"Profile directory not found: {profile_path}"

        # Check for essential profile files
        essential_files = ['Preferences', 'Cookies', 'Web Data']
        missing_files = []

        for file_name in essential_files:
            file_path = os.path.join(profile_path, file_name)
            if not os.path.exists(file_path):
                missing_files.append(file_name)

        if missing_files:
            return False, f"Profile missing essential files: {', '.join(missing_files)}"

        return True, f"Profile accessible: {os.path.basename(profile_path)}"

    except Exception as e:
        return False, f"Error testing profile access: {str(e)}"

def save_profile_preference(profile_path):
    """
    Save the user's profile preference for future use.

    Args:
        profile_path (str): Path to the selected profile
    """
    try:
        pref_file = 'selected_edge_profile.txt'
        with open(pref_file, 'w') as f:
            f.write(profile_path)
        logging.info(f"Saved profile preference to {pref_file}")
    except Exception as e:
        logging.warning(f"Could not save profile preference: {e}")

def load_profile_preference():
    """
    Load the previously saved profile preference.

    Returns:
        str or None: Previously selected profile path, or None if not found
    """
    try:
        pref_file = 'selected_edge_profile.txt'
        if os.path.exists(pref_file):
            with open(pref_file, 'r') as f:
                profile_path = f.read().strip()

            # Verify the profile still exists
            if profile_path == "default" or os.path.exists(profile_path):
                logging.info(f"Loaded saved profile preference: {profile_path}")
                return profile_path
            else:
                logging.warning("Saved profile no longer exists")

    except Exception as e:
        logging.warning(f"Could not load profile preference: {e}")

    return None