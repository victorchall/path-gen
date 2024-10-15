import os
from typing import List, Generator, AsyncGenerator, Tuple
import asyncio


def by_ext(root: str, exts: List[str], recursive: bool = True) -> Generator[str, None, None]:
    """
    Generates pathes for files matching any extension
    """
    assert exts is None or not any(ext is None for ext in exts)
    assert root is not None

    if recursive:
        for root, dirs, files in os.walk(root):
            for file in files:
                if any(file.endswith(ext) for ext in exts):
                    yield os.path.join(root, file)
    else:
        for file in os.listdir(root):
            if any(file.endswith(ext) for ext in exts):
                yield os.path.join(root, file)


async def by_ext_async(root: str, exts: List[str], recursive: bool = True) -> AsyncGenerator[str, None]:
    """
    Generates pathes for files matching any extension, async
    """
    import aiofiles
    assert exts is None or not any(ext is None for ext in exts)
    assert root is not None

    if recursive:
        for root, dirs, files in aiofiles.os.walk(root):
            for file in files:
                if any(file.endswith(ext) for ext in exts):
                    yield os.path.join(root, file)
    else:
        for file in aiofiles.os.listdir(root):
            if any(file.endswith(ext) for ext in exts):
                yield os.path.join(root, file)


def by_ext_first_pairs(root, ext_key: str, paired_exts: List[str], recursive: bool = True)-> Generator[Tuple, None, None]:
    """
    Generates a list of tuples (size 2) of matching files by their path and basename
    First item in tuple will match ext_key file extension
    Second item in tuple matches *first* of any matching file extension in paired_exts

    Parameters:
        ext_key (str): extension for first tuple
        paired_exts (List[str]): extensions to search for first match
    
    """
    assert ext_key is not None
    assert paired_exts is not None
    assert root is not None
    assert not any(ext is None for ext in paired_exts)
    assert not any(ext == ext_key for ext in paired_exts)
    assert not ext_key in paired_exts

    if recursive:
        for dirpath, dirs, files in os.walk(root):
            for file in files:
                for x in _by_ext_first_pairs_one_directory(dirpath, ext_key, paired_exts):
                    yield x

    else:
        for x in _by_ext_first_pairs_one_directory(root, ext_key, paired_exts):
            yield x


def _by_ext_first_pairs_one_directory(root, ext_key: str, paired_exts: List[str])-> Generator[Tuple, None, None]:
    base_name_ext_keys_found = []
    unmatched = {}
    for file in os.listdir(root):
        basename, ext = os.path.splitext(file)
        basename_with_path = os.path.join(root,basename)
        if ext == f".{ext_key}":
            if basename_with_path in unmatched:
                result = f"{basename_with_path}.{ext_key}", unmatched[basename_with_path]
                unmatched.pop(basename_with_path)
                yield result
            else:
                base_name_ext_keys_found.append(basename_with_path)
        elif any(file.endswith(f".{ext}") for ext in paired_exts):
            if basename_with_path in base_name_ext_keys_found:
                base_name_ext_keys_found.pop(basename)
                result = os.path.join(basename_with_path, ext_key), os.path.join(root, file)
                yield result
            else:
                unmatched[basename_with_path] = f"{basename_with_path}{ext}"
