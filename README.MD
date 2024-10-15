# Path-gen

Collection of a few tools used to generate paths to files by extensions or Tuples paired by extensions sets.

### Why?

### _General use_
The package offers a simplified API for iterating over a filesystem when you need specific file extensions in a large file system returned.

This reduces the clutter and boilerplate of code to use os.walk, os.listdir, or other APIs. 

### _Example use case_
When organizing labeled data in machine learning, data may be initially ingested onto a file system with various file extensions based on the source material (ex. web scrape, extractions of other datasets, etc).  For example, image data and their respective labels may be initially saved with various image extensions (webp, png, jpg, jpg_large, etc) and with a label in a txt or json file. 

Dataset packages such as Webdataset expects a fixed set of keys, (ex. (txt + jpg) or (txt + webp) only), packaged into tar containers. They will not function if the dataset has inconsistent extension keys, such as varied image file extensions. This package can bridge the gap for organizing data ahead of time, or can be used for building custom dataloader/dataset classes and functions directly and bypass such limitations.

## Use

### General use

Functions always return a *Generator* class and not a materialized list for performance reasons. Iterate the generator to operate on the results.

        my_generator = path_gen.by_ext(root="/mnt/mypath", exts=["jpg"], recursive=False)

        for file_path in my_generator:
            ...

The results can be materialized into a list if you need, but this may perform poorly for large numbers of paths returned:

        ...
        my_list = list(my_generator)

### Async

Each function has an async version, which leverages aiofile, asyncio, and returns an AsyncGenerator object.

        my_async_generator = path_gen.by_ext_async(root="/mnt/mypath", exts=["jpg"], recursive=False)

        for await file_path in my_async_generator:
            ...

Review the [Python documentation](https://docs.python.org/3/library/asyncio-task.html) on how to get started with async programming or try this [article](https://realpython.com/python-async-features/). 


## Functions

### path_gen.by_extroot(root:str, exts:List[str])

Yields all paths for several different extensions. Directory recursion is default:

    my_generator = path_gen.by_ext(root="/mnt/mypath", exts=["jpg","webp","png"])

    for path in my_generator:
        print(path)
    
      Output:
    /mnt/mypath/image001.jpg
    /mnt/mypath/subfolder/picture001.webp
    ...

Yields all paths for matching file extension *without* directory recursion:

    my_generator = path_gen.by_ext(root="/mnt/mypath", exts=["jpg"], recursive=False)

    for path in my_generator:
        print(path)

      Output:
    /mnt/mypath/image001.jpg
    /mnt/mypath/photo.jpg
    ...

### path_gen.by_ext_first_pairs(root:str, ext_key:str, paired_exts:List[str])

Yields tuples of size 2 where path and baseame is the same, ex. 

_[("file1.my_key_ext", "file1.my_paired_ext"), ..., ("some/path/file99.my_key_ext","some/path/file99.my_paired_ext")]_

The function is gauranteed to only return tuples of size 2, and the first item in each tuple must have the **ext_key** file extension, and the second item is guaranteed to match *one of* the **paired_exts** values.

**ext_key** must not match any item in **paired_exts**

    my_generator = path_gen.by_ext_first_pairs(root="./mypath", ext_key="ext1", paired_exts=["ext2"])

When more than one paired_exts is supplied, the *first match* from paired_ext is returned with its respective key_ext.  Which paired_ext is returned if more than one match exists will depend on the order operating system returns them.

    my_generator = path_gen.by_ext_first_pairs(root="./mypath", ext_key="ext1", paired_exts=["ext2","ext3"])

If no paired_ext is found for a given matched file my ext_key, then that ext_key will not be returned. 

