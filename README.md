# Senaps Fast App Generator


sfgen is a console application to quickly generate the basic structure of a application.

## install

since we ain't online on `pypi`, you should download the source, unzip it, move into the directory and and install it using the pip.

    pip install .

after this, you can use `sfgen` by invoking it's command arguments.

## usage
to use `sfgen`, there is only one option for now, but we will be building on it in the future.
**remember** that you should create a `virtualenv` for the project yourself. 

### create
create app creates a new flask application, blueprint ready .

    sfgen create flask
this will create a folder named `flask_bare-0.0.1-alpha` and within it, is the `flask` files you would need to use.

#### options

    sfgen create module -n sample -o /root/sampleproject

- **` -n --name`** the project name, this will be used as the folder name too.
- **` -o --path`** this is the path to put the project in(not implemented yet!)


## app options

currently i only have only implemented the `flask` and `module`. but will build upon them.