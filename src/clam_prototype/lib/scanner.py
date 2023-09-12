# A wrapper around calling clamdscan


import subprocess

from lib import fast_log


def validate_clamdscan() -> bool:
    """
    :return: True if clamdscan is available, False otherwise
    """

    result = subprocess.run(['which', 'clamdscan'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    if result.returncode != 0:
        return False

    return True


def _run_clamdscan(path: str) -> (bool, str):
    """
    :param path: A path to scan
    :return: True if no virus is found, False otherwise
    """

    # --fdpass here is needed since by default, the unpacker runs as root
    result = subprocess.run(['clamdscan', '-m', '--stdout', path], capture_output=True, text=True)

    if result.returncode != 0:
        return False, result.stdout

    return True, ""


def clamdscan(paths: list[str], fail_fast: bool) -> bool:
    """
    :param paths: A list of paths to scan
    :param fail_fast: If true, will stop scanning after the first failure
    :return: True if no virus is found, False otherwise
    """

    paths_clean = True

    for a_path in paths:
        fast_log.info(f'Scanning {a_path}')
        is_clean, clamdscan_output = _run_clamdscan(a_path)
        if not is_clean:
            paths_clean = False
            fast_log.error('!' * 80)
            fast_log.error(f'Viruses found by clamdscan in file {a_path}:')
            fast_log.error(clamdscan_output)
            fast_log.error('!' * 80)
            if fail_fast:
                return False

    if paths_clean:
        fast_log.info('=' * 80)
        fast_log.info('No viruses found by clamdscan, all clear!')
        fast_log.info('=' * 80)

    return paths_clean
