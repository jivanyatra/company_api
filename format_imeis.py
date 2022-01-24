from sys import stdin
import re
import click

def parser(*, data):
    """Takes input from command-line as a list of lines, 
    parses line-by-line for IMEIs (15 digits) using regex
    and returns them as a list of strings
    """
    imei_pattern = r"[0-9]{15}"
    output = []
    for line in data:
        line = line.strip()
        match = re.match(imei_pattern, line)
        if match:
            output.append(match.group(0))
    return output

@click.command()
@click.option('-q', 'output', flag_value='quoted', default=True, help="Quoted, multi-line (default)")
@click.option('-b', 'output', flag_value='bare', help="Bare, multi-line")
@click.option('-s', 'output', flag_value='spaces', help="Space separated, single-line")
@click.option('-c', 'output', flag_value='commas', help="Comma separated, single-line")
@click.option('-j', 'output', flag_value='json', help="JSON-ready (quoted and comma separated, single-line")
def format_imeis(output):
    """This script asks for input of text, parses one IMEI per
    line, and then outputs in one of four ways:\n
    1) (Default) "IMEI" (multi-line)\n
    2) IMEI (multi-line)\n
    3) IMEI1 IMEI2 IMEI3 (single-line)\n
    4) IMEI1, IMEI2, IMEI3 (single-line)\n
    5) "IMEI1", "IMEI2", "IMEI3" (single-line)\n
    """
    
    quoted_commad_output = '"{}"'
    bare_output = "{}"
    single_line_spaces = " ".join
    single_line_commas = ", ".join
    
    click.echo("Enter IMEIs (CTRL+D to finish)>> ", nl=False)
    inp = stdin.readlines()
    click.echo("<< End of Input")
    click.echo()
    click.echo()
    
    parsed_data = parser(data=inp)
    
    if output == 'quoted':
        for imei in parsed_data:
            click.echo(quoted_commad_output.format(imei))
            
    elif output == 'bare':
        for imei in parsed_data:
            click.echo(bare_output.format(imei))
            
    elif output == 'spaces':
        click.echo(single_line_spaces(parsed_data))
        
    elif output == 'commas':
        click.echo(single_line_commas(parsed_data))
        
    elif output == 'json':
        click.echo(single_line_commas([f'"{imei}"' for imei in parsed_data]))
            
    click.echo()
    click.echo()

if __name__ == "__main__":
    format_imeis()