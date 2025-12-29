import click
from gva_cli.embeddings import getEmbeddings, Search, getPaths, updateFolder, Search_All
from pathlib import Path
import subprocess
import os

@click.group()
def cli():
    pass


@cli.command()
def embed():
    getEmbeddings()

@cli.command()
@click.argument('prompt')
def search(prompt):
    results= Search(prompt)

    print("\n")

    if(results):
        print("Top Results:")
        print("______________________________________________________________________________")
        for i in results:
            print(i)

        print("\n")

    else:
        print("Not found. Run embed first")




@cli.command(name="sync")
def sync_folder():
    base_dir= Path(__file__).resolve().parent
    db_exe= base_dir/ "FileTraversal" / "db_exe"
    path= Path.cwd()
    db= path / "embeddings.db"

    subprocess.run(
        [str(db_exe), str(db), str(path)],
        check=True
    )

    count= updateFolder()

    print("Insertions: ",count)


@cli.command(name="open")
@click.argument('image')
def open_image(image):
    base_dir= Path(__file__).resolve().parent
    IO= base_dir/ "FileTraversal" / "IO"

    path= Path.cwd()
    image_path= path / image

    subprocess.run(
        [str(IO), str(image_path)],
        check=True
    )








@cli.command()
@click.argument('image_folder', type=click.Path(exists=True))
def update(image_folder):
    status= updateFolder(image_folder)

    if(status== "Success"):
        print("New images saved")



if __name__ == '__main__':
    cli()