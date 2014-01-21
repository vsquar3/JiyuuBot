def git(self, message):
    import requests
    matches = re.findall("github.com/([\w/-]+[^\s])", message)
    for match in matches:
        match = match.split("/")
        if match[-1] == "":
            del match[-1]
        if len(match) == 1:
            req = requests.get("http://osrc.dfm.io/%s.json" % match[0]).json()
            if not "message" in req.keys():
                self.conman.gen_send("Github: %s - %s repositories - %s contributions - Favourite language: %s (%s contributions)" % (req["name"], len(req["repositories"]), req["usage"]["total"], req["usage"]["languages"][0]["language"], req["usage"]["languages"][0]["count"]))
            else:
                req = requests.get("https://api.github.com/users/%s" % match[0]).json()
                if not "message" in req.keys():
                    self.conman.gen_send("Github: %s" % req["login"])
                else:
                    self.conman.gen_send("Github: User %s doesn't appear to exist" % match[0])
        elif len(match) == 2:
            req = requests.get("https://api.github.com/repos/%s/%s" % tuple(match)).json()
            tosend = "Github: %s - %s - by %s - Last push: %s" % (match[1], req["description"], match[0], req["pushed_at"].split("T")[0])
            if not req["homepage"] == None and not req["homepage"] == "":
                tosend += " - %s" % req["homepage"]
            self.conman.gen_send(tosend)
        elif match[2] == "issues" or match[2] == "pull":
            match[2] = "issues"
            if len(match) == 4:
                req = requests.get("https://api.github.com/repos/%s/%s/%s/%s" % tuple(match)).json()
                self.conman.gen_send("Github: %s/%s#%s - %s - by %s - Created: %s - Updated: %s" % (match[0], match[1], req["number"], req["title"], req["user"]["login"], req["created_at"].split("T")[0], req["updated_at"].split("T")[0]))
            else:
                req = requests.get("https://api.github.com/repos/%s/%s/%s" % tuple(match)).json() 
                numofiss = len(req)
                self.conman.gen_send("Github: %s - by %s - Open issues: %s" % (match[1], match[0], numofiss))
        elif match[2] == "tree":
            branch = match[3]
            filepath = "/".join(match[4:])
            self.conman.gen_send("Github: %s on branch %s - %s - by %s" % (filepath, branch, match[1], match[0]))
        elif match[2] == "commit":
            req = requests.get("https://api.github.com/repos/%s/%s/%ss/%s" % tuple(match)).json()
            self.conman.gen_send("Github: Commit %s on %s/%s - %s - by %s - %s" % (req["sha"], match[0], match[1], req["message"], req["author"]["name"], req["commiter"]["date"].split("T")[0]))

self._map("regex", ".*https?://(www\.)?github.com/.*", git)
