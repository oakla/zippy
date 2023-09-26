

import subprocess

wzzip_path = r"c:\program files\winzip\wzzip"
TO_ZIP = r'C:\Users\Alexander.Oakley\my-stuff-noonedrive\Code\proj\py-boom-zip\scratch\output\test_zip.zip'
IN_FOLDER = r'C:\Users\Alexander.Oakley\my-stuff-noonedrive\Code\proj\py-boom-zip\test\inputs'

subprocess.run([
    wzzip_path, TO_ZIP, IN_FOLDER
], shell=True)