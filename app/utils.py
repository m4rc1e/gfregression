import os
import re
import shutil
import requests
import json
try:
    from StringIO import StringIO
except ModuleNotFoundError:  # py3 workaround
    from io import BytesIO as StringIO

# Info taken from https://caniuse.com/#feat=variable-fonts
MIN_VF_BROWSERS = {
    'chrome': 67,
    'firefox': 62,
    'edge': 17,
    'safari': 11,
}

current_dir = os.path.dirname(__file__)

with open(os.path.join(current_dir, "gf_families_ignore_camelcase.json")) as f:
    GF_FAMILY_IGNORE_CAMEL = json.loads(f.read())


GF_STYLE_TERMS = {
    'Thin': 'Thin',
    'ExtraLight': 'Extralight',
    'Light': 'Light',
    'Regular': 'Regular',
    'Medium': 'Medium',
    'SemiBold': 'SemiBold',
    'Bold': 'Bold',
    'ExtraBold': 'ExtraBold',
    'Black': 'Black',
    'ThinItalic': 'Thin Italic',
    'ExtraLightItalic': 'ExtraLight Italic',
    'LightItalic': 'Light Italic',
    'Italic': 'Italic',
    'MediumItalic': 'MediumItalic',
    'SemiBoldItalic': 'SemiBold Italic',
    'BoldItalic': 'Bold Italic',
    'ExtraBoldItalic': 'ExtraBold Italic',
    'BlackItalic': 'Black Italic',
}


def browser_supports_vfs(user_agent):
    """Check if the user's browser supports variable fonts

    Parameters
    ----------
    user_agent: werkzeug.useragents.UserAgent

    Returns
    -------
    Boolean"""
    user_browser = user_agent.browser
    browser_version = int(user_agent.version.split('.')[0])
    if user_browser not in MIN_VF_BROWSERS:
        return False
    if browser_version < MIN_VF_BROWSERS[user_browser]:
        return False
    return True


def download_file(url, dst_path=None):
    """Download a file from a url. If no url is specified, store the file
    as a StringIO object"""
    request = requests.get(url, stream=True)
    if not dst_path:
        return StringIO(request.content)
    with open(dst_path, 'wb') as downloaded_file:
        shutil.copyfileobj(request.raw, downloaded_file)


def family_name_from_filename(filename, seperator=' '):
    """RubikMonoOne-Regular > Rubik Mono One"""
    family = filename.split('-')[0]
    if family not in list(GF_FAMILY_IGNORE_CAMEL.keys()):
        return re.sub('(?!^)([A-Z]|[0-9]+)', r'%s\1' % seperator, family)
    else:
        return GF_FAMILY_IGNORE_CAMEL[family]


def style_name_from_filename(filename, seperator=' '):
    """RubikMonoOne-Regular --> Regular"""
    try:
        style = filename.split('-')[1]
        return GF_STYLE_TERMS[style]
    except:
        return 'Regular'


with open(os.path.join(current_dir, "secrets.json")) as f:
    secrets = json.loads(f.read())

def secret(key, secret=secrets):
    try:
        return secret[key]
    except KeyError:
        raise Exception('Secret {} does not exist'.format(secret))
