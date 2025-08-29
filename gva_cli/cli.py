import click
from gva_cli.embeddings import getEmbeddings, Search, getPaths, updateFolder, Search_All

@click.group()
def cli():
    pass


@cli.command()
@click.argument('image_folder', type=click.Path(exists=True))
def embed(image_folder):
    getEmbeddings(image_folder)

@cli.command()
@click.argument('image_folder', type=click.Path(exists=True))
@click.argument('prompt')
def search(image_folder, prompt):
    results= Search(image_folder, prompt)

    print("\n")

    if(results):
        print("Top Results:")
        print("______________________________________________________________________________")
        for i in results:
            print(i)

        print("\n")

    else:
        print("Not found. Run embed first")

@cli.command(name="search-all")
@click.argument('prompt')
def search_all(prompt):
    results= Search_All(prompt)

    print("\n")

    if(results):
        print("Top Results:")
        print("______________________________________________________________________________")
        for i in results:
            print(i)

        print("\n")


    else:
        print("Not found. Run embed first")













@cli.command(name="get-paths")
def get_paths():
    paths=getPaths()

    if(paths):
        print("\n")
        for path in paths:
            print(path)

        print("\n")

    else:
        print("No folders embedded")


@cli.command()
@click.argument('image_folder', type=click.Path(exists=True))
def update(image_folder):
    status= updateFolder(image_folder)

    if(status== "Success"):
        print("New images saved")



if __name__ == '__main__':
    cli()