# Background information

when you see the header format, you may ask why I didnt use `http`. To be fair there was no reason I couldn't use http as is. I just wanted to use a completely different way of encryption than what https would use. I think it would be better to never send your password over the network in any way.

---

# Header Format

```yaml
# \r\n line seperator
# Must have a length of the headsize defined in data/config.toml
request-type: GET/SET/RESPONSE
content-type: json/binary
file-name: None/file name
server: none/ServerName
time: unix date time format
```

# Handshake (GET)
This is one of the only irregular packets.

header
```yaml
request-type: SET
content-type: json
file-name: None
server: None
time: t
```
content
```json
{
    "user" : "taustin",
    "sample" : "'HandShake' encoded with users encryption key. This allows you to know if you got the password correct."
}
```
^ yes, this is just the word "HandShake" encoded
## response
header
```yaml
request-type: RESPONSE
content-type: json
file-name: None
server: None
time: t
```
content
```json
{
    "accepted": true,
    "response": "Error message if there is one"
}
```

possible errors
```json
"Password or keyfile incorrect, please try again",
"Too many login attempts have been tried in the past 30 minutes, please try again in 30 minutes."
```

The latter of these will be sent within 10 incorrect tries.

---

# sync Git Repo (SET)

this tells the server to run a git fetch

header
```yaml
request-type: SET
content-type: json
file-name: None
server: ServerName
time: t
```
content
```json
{
    "action": "git",
    "args"  : {
        "git_action": "sync"
    }
}
```