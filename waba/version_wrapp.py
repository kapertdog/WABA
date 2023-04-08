# https://pypi.org/project/pyinstaller-versionfile/
import pyinstaller_versionfile
import info


def wrapp():
    pyinstaller_versionfile.create_versionfile(
        output_file=info.versionfile_path,
        version=info.version.semver(),
        company_name=info.company,
        file_description=info.description,
        internal_name=info.shortname,
        legal_copyright=info.legal_copyright,
        original_filename=info.exe_name,
        product_name=info.shortname,
    )


if __name__ == '__main__':
    wrapp()
