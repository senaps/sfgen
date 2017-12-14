# Senaps Flask Generator


sfgen is a console application to quickly generate the basic structure of a blueprint ready flask application.

## install

since we ain't online on `pypi`, you should download the source, unzip it, move into the directory and and install it using the pip.

    pip install .

after this, you can use `sfgen` by invoking it's command arguments.

## usage
to use `sfgen`, there is only one option for now, but we will be building on it in the future.
**remember** that you should create a `virtualenv` for the project yourself. 

### create_app
create app creates a new flask application, blueprint ready .

    sfgen create_app
this will create a folder named `test` and within it, is the `flask` files you would need to use.

#### options

- **`-name`** the project name, this will be used as the folder name too.
- **`-path`** this is the path to put the project in(not implemented yet!)

## update
to update the `sfgen` application, and since it's not present in `pypi`, you would have to download the updated version and upgrade it with:

    pip install -U .
and this command will update `sfgen`

## contribution
although this is a personal project, every contribution is welcome.

### sfgen needs
- **`tests`** for the `sfgen` app itself, or the `flask_bare` application that it generates
- **`code style`** improvements so the code can be read and used more easily
- **`refactoring`** codes so it's more and more dynamic and be more usable for different usages. 
