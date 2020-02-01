Feature: Test feature
Scenario: Test scenario
  Given website 'https://www.google.ru'
  Then check google search field exists
  When enter google query 'Центральный банк РФ'
  And click google submit
  Then check link exists 'cbr.ru'
  When click link 'cbr.ru'
  Then check url 'https://www.cbr.ru'
  When click reception
  And click gratitude
  And enter message 'случайный текст'
  And checkbox agree
  Then take screenshot
  When click menu
  And click about
  And click warning
  Then save warning
  When switch language to en
  Then compare warning text
  And take screenshot