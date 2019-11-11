import re

def generateCommand(command):
    if re.match(r"clicker click", command):
        m = re.match("^clicker\sclick\sat\s(\d.*)\s(\d.*)$", command)
        if m:
            return """
            window.gremlins.species.clicker()
            .clickTypes(['click'])
            .positionSelector(function() {
                return [parseInt(%s), parseInt(%s)];
            })
            .randomizer(new Chance())
            .logger({log: function(msg) { console.log(msg) }})();
            """ % (m.group(1),m.group(2))
    elif re.match(r"clicker dblclick", command):
        m = re.match("^clicker\sdblclick\sat\s(\d.*)\s(\d.*)$", command)
        if m:
            return """
            window.gremlins.species.clicker()
            .clickTypes(['dblclick'])
            .positionSelector(function() {
                return [parseInt(%s), parseInt(%s)];
            })
            .randomizer(new Chance())
            .logger({log: function(msg) { console.log(msg) }})();
            """ % (m.group(1),m.group(2))
    elif re.match(r"clicker mousedown", command):
        m = re.match("^clicker\smousedown\sat\s(\d.*)\s(\d.*)$", command)
        if m:
            return """
            window.gremlins.species.clicker()
            .clickTypes(['mousedown'])
            .positionSelector(function() {
                return [parseInt(%s), parseInt(%s)];
            })
            .randomizer(new Chance())
            .logger({log: function(msg) { console.log(msg) }})();
            """ % (m.group(1),m.group(2))
    elif re.match(r"clicker mouseup", command):
        m = re.match("^clicker\smouseup\sat\s(\d.*)\s(\d.*)$", command)
        if m:
            return """
            window.gremlins.species.clicker()
            .clickTypes(['mouseup'])
            .positionSelector(function() {
                return [parseInt(%s), parseInt(%s)];
            })
            .randomizer(new Chance())
            .logger({log: function(msg) { console.log(msg) }})();
            """ % (m.group(1),m.group(2))
    elif re.match(r"clicker mouseover", command):
        m = re.match("^clicker\smouseover\sat\s(\d.*)\s(\d.*)$", command)
        if m:
            return """
            window.gremlins.species.clicker()
            .clickTypes(['mouseover'])
            .positionSelector(function() {
                return [parseInt(%s), parseInt(%s)];
            })
            .randomizer(new Chance())
            .logger({log: function(msg) { console.log(msg) }})();
            """ % (m.group(1),m.group(2))
    elif re.match(r"clicker mousemove", command):
        m = re.match("^clicker\smousemove\sat\s(\d.*)\s(\d.*)$", command)
        if m:
            return """
            window.gremlins.species.clicker()
            .clickTypes(['mousemove'])
            .positionSelector(function() {
                return [parseInt(%s), parseInt(%s)];
            })
            .randomizer(new Chance())
            .logger({log: function(msg) { console.log(msg) }})();
            """ % (m.group(1),m.group(2))
    elif re.match(r"clicker mouseout", command):
        m = re.match("^clicker\smouseout\sat\s(\d.*)\s(\d.*)$", command)
        if m:
            return """
            window.gremlins.species.clicker()
            .clickTypes(['mouseout'])
            .positionSelector(function() {
                return [parseInt(%s), parseInt(%s)];
            })
            .randomizer(new Chance())
            .logger({log: function(msg) { console.log(msg) }})();
            """ % (m.group(1),m.group(2))  
    return None