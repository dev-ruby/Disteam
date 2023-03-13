<div align="center">

# Disteam


![Alt text](https://img.shields.io/github/languages/code-size/dev-ruby/Disteam)
![Alt text](https://img.shields.io/github/directory-file-count/dev-ruby/Disteam)
![Alt text](https://img.shields.io/tokei/lines/github/dev-ruby/disteam)


![Alt text](https://img.shields.io/github/issues/dev-ruby/disteam)
![Alt text](https://img.shields.io/github/commit-activity/m/dev-ruby/disteam)

Disteam, 디스팀은 SteamAPI를 이용한 여러 기능들을 디스코드에서 사용할 수 있도록 하는 봇입니다.

[초대하기](https://discord.com/api/oauth2/authorize?client_id=1074267701461139486&permissions=83968&scope=bot)


</br>
</br>
</br>
</br>
</br>


## 명령어

### $RecentGame `user_id` | `profile_url`
`user_id` : 스팀 id
`profile_url` : 프로필 링크

</br>
</br>

해당 유저가 최근 플레이한 게임 3개의 정보를 불러옵니다.

`IPlayerService/GetRecentlyPlayedGames`, `ISteamUser/GetPlayerSummaries`, `ISteamUser/ResolveVanityURL` API를 사용합니다.

![Alt text](https://github.com/dev-ruby/Disteam/blob/main/preview/RecentGame_Screenshot.png)
