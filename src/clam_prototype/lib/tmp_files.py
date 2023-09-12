import glob
import os
import tempfile

from lib.file_data import FileMetadata, FileType

TMP_FILE_PREFIX = 'clam_unpacker'


# Makes a temporary directory for the file to be unpacked into, named base on filetype and filename
def make_temp_dir(file_meta: FileMetadata, tmp_dir: str) -> str:
    if not file_meta.root_meta:
        prefix = f'{TMP_FILE_PREFIX}_{file_meta.filetype.get_filetype_short()}_{file_meta.get_filename()}_'
    else:
        prefix = f'{TMP_FILE_PREFIX}_{file_meta.filetype.get_filetype_short()}-p_{file_meta.root_meta.get_filename()}_p-{file_meta.get_filename()}_'
    tmp_dir = tempfile.mkdtemp(prefix=prefix, dir=tmp_dir)

    # Need to make it readable by everyone, otherwise clam will throw a fit
    os.chmod(tmp_dir, 0o755)

    return tmp_dir


# Determine the filetype based on the path, assuming that it was created by make_temp_dir
def determine_filetype(path: str) -> FileType:
    for filetype in FileType:
        if os.path.basename(path).startswith(f'{TMP_FILE_PREFIX}_{filetype.get_filetype_short()}'):
            return filetype

    return FileType.UNKNOWN


# Find all the directories created by make_temp_dir that are associated with the given file
def find_associated_dirs(filepath: str, tmp_dir: str) -> list[str]:
    file_name = os.path.basename(filepath)
    return glob.glob(f'{tmp_dir}/{TMP_FILE_PREFIX}_*_{file_name}_*')
