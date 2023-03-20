# DISTEAM-ALT

![Alt text](https://img.shields.io/github/languages/code-size/Sharp0802/Disteam)
![Alt text](https://img.shields.io/github/directory-file-count/Sharp0802/Disteam)
![Alt text](https://img.shields.io/tokei/lines/github/Sharp0802/disteam)
![Alt text](https://img.shields.io/github/issues/Sharp0802/disteam)
![Alt text](https://img.shields.io/github/commit-activity/m/Sharp0802/disteam)

## SUMMARY

`Disteam`: 
A discord bot that provides you ways to access Steam API in discord, 
written in python3,
for cross-platform.

`Disteam-Alt`:
A fork of `Disteam` that improve the readability of source code and make source code more object-driven.

## GOAL

- Improve the readablity of original source code
- Make more object-driven
- Optimize performance

## SYNOPSIS

### Get the 3 most-recently-played games of specific user

<pre>
$RecentGame [<i>USER-ID</i> | <i>PROFILE-URL</i>]
</pre>

### Get the profile info of specific user

<pre>
$Profile [<i>USER-ID</i> | <i>PROFILE-URL</i>]
</pre>

## DESCRIPTION

> Basically, The usage and internal method is same as original project.
>
> Only difference is that this is refactored version of original source.

### `$RecentGame` command

The `$RecentGame` command retrieves the 3 most-recently-played games of specific user.
User can be specified by `USER-ID` parameter or `PROFILE-URL` parameter.

```
$RecentGame 76561199057515902
```

Callee(`Disteam` host) will detect whether that parameter is `USER-ID` or `PROFILE-URL` via determine if parameter is valid URL.
For example, `76561199057515902` is invalid URL.
Thus, Callee will consider parameter as `USER-ID`.
Otherwise, Callee will query `USER-ID` with sending GET request to url.

Callee will use steam API: 
- `IPlayerService/GetRecentlyPlayedGames`
- `ISteamUser/GetPlayerSummaries`
- `ISteamUser/ResolveVanityURL`

### `$Profile` command

The `$Profile` command will show you the profile info of specific user.
User can be specified by `USER-ID` parameter or `PROFILE-URL` parameter.

```
$Profile 76561199057515902
```

Callee(`Disteam` host) will detect whether that parameter is `USER-ID` or `PROFILE-URL` via determine if parameter is valid URL.
For example, `76561199057515902` is invalid URL.
Thus, Callee will consider parameter as `USER-ID`.
Otherwise, Callee will query `USER-ID` with sending GET request to url.

Callee will use steam API: 
- `IPlayerService/GetOwnedGames`
- `ISteamUser/GetPlayerSummaries`
- `IPlayerService/GetSteamLevel`
- `ISteamUser/ResolveVanityURL`


## PREVIEW

### View recent 3 games

![Alt text](https://raw.githubusercontent.com/dev-ruby/Disteam/main/preview/RecentGame_Screenshot.png)

### View profile info

![Alt text](https://raw.githubusercontent.com/dev-ruby/Disteam/main/preview/Profile_Screenshot.png)
