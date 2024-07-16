import sounddevice as sd
import scipy
import click

@click.group()
def cli():
    pass


@click.command()
def record_warno_vo():
    print("Record Warno VO")
    # TODO go through each voice line one by one
    # TODO press spacebar to start/stop the recording of each and save to the right place as an ogg file
    # TODO have a param to filter files by filename/prefix, to overwrite them or not so we can continue where we left off, 
    pass


cli.add_command(record_warno_vo)

if __name__ == "__main__":
    cli()
