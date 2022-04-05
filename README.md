# keylight-cli

A Python CLI module designed to control the [Elgato](https://www.elgato.com/en) brand Lights. Use this when you want a simple command line to control your keylight. Currently only tested with a Keylight Air

## Dependencies
This uses the excellent [leglight](https://gitlab.com/obviate.io/pyleglight) python module, and wraps it in a very simple CLI tool.

## Usage
The CLI supports multiple keylights on a single network. You can target a specific light with a `-s <serial number>` parameter before any command. 
If no serial number is provided, then the CLI will use the first one found on the network (not necessarily guaranteed to be the same one each time).
For best results, specify the serial number if you have multiple keylights to control

Run the command without any arguments to see the help

### List

```
% keylight list
Found 1 lights
Light <SERIAL> at <IP>:<PORT>
```

### Info

```
% keylight info
Getting information from <SERIAL>
Light <SERIAL> at <IP>:<PORT>
State             : ON
Brightness        : 10 %
Color Temperature : 4300.0 K
```

### Control
```
% keylight on
Turning on <SERIAL>
% keylight off
Turning off <SERIAL>
```


### Brightness
```
% keylight set-brightness 50
Setting brightness for <SERIAL> to 50%
```

### Color Temperature
```
% keylight set-color-temperature 5000
Setting color temperature for <SERIAL> to 5000K
```

## License
MIT

## Copyright
Elgato, Key Light and other product names are copyright of their owner, CORSAIR. 
