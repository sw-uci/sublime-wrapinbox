import sublime
import sublime_plugin

class BoxDrawingSelectionCommand(sublime_plugin.TextCommand):
    cornertype = {
        "normal": {
            "tl": '┌',
            "tr": '┐',
            "bl": '└',
            "br": '┘',
        },
        "round": {
            "tl": '╭',
            "tr": '╮',
            "bl": '╰',
            "br": '╯',
        },
        "ascii": {
            "tl": '+',
            "tr": '+',
            "bl": '+',
            "br": '+',
        },
    }
    linetype = {
        "normal": {
            "horiz": '─',
            "vert": '│',
        },
        "dashed": {
            "horiz": '┈',
            "vert": '┊',
        },
        "ascii": {
            "horiz": '-',
            "vert": '|',
        }
    }

    def run(self, edit, **args):
        straight = self.__class__.linetype[args.get("straight", "normal")]
        corner   = self.__class__.cornertype[args.get("corner", "normal")]

        for i, region in enumerate(self.view.sel()):
            if region.size() > 0:
                if i == 0:
                    s = self.view.substr(region)
                    if len(s) == 1:
                        s = straight["vert"]
                    else:
                        s = straight["horiz"] * len(s)
                        if len(s) > 1:
                            s = corner["tl"] + s[:-2] + corner["tr"]
                    self.view.replace(edit, region, s)
                else:
                    # middle rows
                    self.view.replace(edit, sublime.Region(region.begin(), region.begin()+1), straight["vert"])
                    self.view.replace(edit, sublime.Region(region.end()-1, region.end())    , straight["vert"])

        # final row
        # will execute even if it's the only row
        if region.size() > 0:
            s = self.view.substr(region)
            if len(s) == 1:
                # if selection width is len 1, just draw a vertical line
                s = straight["vert"]
            else:
                s = straight["horiz"] * len(s)
                # draw corners if total selection spans more than one line
                # else just leave it as a horizontal line
                if i > 0:
                    if len(s) > 1:
                        s = corner["bl"] + s[:-2] + corner["br"]
            self.view.replace(edit, region, s)
