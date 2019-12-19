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

    sfgen simple
this will create a simple project for you in the current path where you are. the project will be named `app`

#### options

    sfgen -n blog -p /tmp simple

- **` -n --name`** the project name, this will be used as the folder name too.
- **` -p --path`** this is the path to put the project in


## app options

currently i only have only implemented the `simple` flask app. but will come up with a `full` app too which contains the whole setup for blueprints and all.

## TODO:
- [ ] the tests and coverage
- [ ] more apps to be supported
- [ ] code documentation and refactoring