""" Generate Memes """

import os
from userge.utils import secure_env

IMGFLIP_ID = os.environ.get(secure_env("IMGFLIP_ID"))
IMGFLIP_PASS = os.environ.get(secure_env("IMGFLIP_PASS"))
