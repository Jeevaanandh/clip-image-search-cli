import click
from Embeddings import getEmbeddings, Search, getPaths

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

    if(results):
        print("Top Results:")
        for i in results:
            print(i)

    else:
        print("Not found. Run embed first")


@cli.command(name="get-paths")
def get_paths():
    paths=getPaths()

    if(paths):
        for path in paths:
            print(path)

    else:
        print("No folders embedded")


if __name__ == '__main__':
    cli()