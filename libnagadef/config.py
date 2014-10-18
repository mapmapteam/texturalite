#!/usr/bin/env python
import os
import yaml

class VideoCue(object):
    """
    One video cue.
    """
    def __init__(self):
        self.uri = ""
        self.duration = 10.0

    def __str__(self):
        ret = str(self.__dict__)
        return ret


class Configuration(object):
    """
    The configuration options for this application.
    Mostly contains the cue list.
    """
    def __init__(self):
        self.verbose = False
        self.directory = "."
        self.osc_port = 54321
        self.cues = []

    def __str__(self):
        ret = ""
        ret = "verbose = " + str(self.verbose) + "\n"
        ret = "directory = " + str(self.directory) + "\n"
        ret = "osc_port = " + str(self.osc_port) + "\n"
        ret += "cues = ["
        for cue in self.cues:
            ret += str(cue) + "," 
        ret += "]\n"
        return ret


def parse_one_cue(d, directory="."):
    """
    Parse one cue in the JSON dict.
    @raise RuntimeError
    """
    ret = VideoCue()
    keys = ret.__dict__.keys()
    for k in keys:
        _type = type(ret.__dict__[k])
        if d.has_key(k):
            # Might raise a TypeError or a ValueError:
            try:
                v = _type(d[k])
            except ValueError, e:
                raise RuntimeError("Invalid value for key %s: %s" % (k, e))
            except TypeError, e:
                raise RuntimeError("Invalid value for key %s: %s" % (k, e))

            ret.__dict__[k] = v
            if k == "uri":
                uri = os.path.join(directory, v)
                if not os.path.exists(uri):
                    print("Warning: Video file not found: %s" % (uri))
                ret.__dict__[k] = uri
            if k == "duration":
                if v < 0.1:
                    ret.__dict__[k] = 0.1
    return ret


def load_from_file(config_file_path=None):
    """
    Load Configuration from JSON file.
    @raise RuntimeError
    """
    ret = Configuration()
    if config_file_path is None:
        config_file_path = os.path.expanduser("~/.videocontrol")
    if os.path.exists(config_file_path):
        f = open(config_file_path)
        try:
            data = yaml.load(f)
        except ValueError, e:
            raise RuntimeError("Error parsing configuration file %s: %s" % (config_file_path, e))
        f.close()
        # the videos directory first
        try:
            ret.directory = os.path.expanduser(data["directory"])
        except KeyError:
            print("No key %s key in config file" % ("directory"))
        try:
            cues = data["videos"]
            for item in cues:
                cue = parse_one_cue(item, ret.directory)
                ret.cues.append(cue)
        except RuntimeError, e:
            raise RuntimeError("Error parsing configuration file %s: %s" % (config_file_path, e))
        except IndexError, e:
            raise RuntimeError("Error parsing configuration file %s: %s" % (config_file_path, e))
        except KeyError, e:
            raise RuntimeError("Error parsing configuration file %s: %s" % (config_file_path, e))

    else:
        raise RuntimeError("Configuration file path doesn't exist: %s" % (config_file_path))
    return ret


if __name__ == "__main__":
    # Just to test it quickly
    fname = "sample_config.yaml"
    config = load_from_file(fname)
    print(str(config))

