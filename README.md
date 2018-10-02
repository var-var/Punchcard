Consume the username on the github, for example, kraih.
 You need to take all the user repositories using
 the GitHub API (https://api.github.com/users/kraih/repos),
 for each repository take a list of commits (https://api.github.com/ repos / kraih / mojo-pg / commits)
 and build a table of activity commits: vertically days of the week,
 horizontally hours, on intersection - the number of commits.
 For each repository, collect information for the last year and accurately output it to the console.

Скрипту​ ​на​ ​вход​ ​подается​ ​логин​ ​пользователя​ ​на​ гитхабе,​ например kraih​.​
 ​Нужно​ ​с помощью​ ​GitHub​ ​API​ ​взять​ ​все​ ​репозитории​ ​пользователя (https://api.github.com/users/kraih/repos),​
 ​по​ ​каждому​ ​репозиторию​ ​взять список​ ​коммитов​ ​(​https://api.github.com/repos/kraih/mojo-pg/commits​)​
 и построить​ ​таблицу​ ​активности​ ​коммитов:​ ​по​ ​вертикали​ ​дни​ ​недели,​ ​по​ ​горизонтали часы,​
 ​на​ ​пересечении​ ​—​ ​количество​ ​коммитов.​ ​По​ ​каждому​ ​репозиторию​ ​собрать информацию​ ​за​ ​год​ ​назад​
 ​и​ ​аккуратно​ ​вывести​ ​это​ ​в​ ​консоль.