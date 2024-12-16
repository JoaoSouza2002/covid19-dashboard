### Creates (partial) functions for every Android activity using ADB 

```python
pip install a-pandas-ex-adb-execute-activities

from a_pandas_ex_adb_execute_activities import pd_add_adb_execute_activities

pd_add_adb_execute_activities()
import pandas as pd

packagename = "com.google.android.youtube"
adb_path = "C:\\Users\\Gamer\\AppData\\Local\\Android\\Sdk\\platform-tools\\adb.exe"
deviceserial = "localhost:5745"
df = pd.Q_ADB_activities_from_package_to_df(adb_path, deviceserial, packagename)
df2 = pd.Q_ADB_all_activities_to_df(adb_path, deviceserial)

#Overview 
df.com_google_android_youtube_com_google_android_apps_youtube_app_application_Shell_UploadActivity__UPLOAD__DEFAULT__video
Out[19]: 
package             com.google.android.youtube/com.google.android....
Action                com.google.android.youtube.intent.action.UPLOAD
AutoVerify                                                      false
Category                              android.intent.category.DEFAULT
Type                                                            video
mHasPartialTypes                                                 true
mPriority                                                           0
Scheme                                                               
command             am start -a "com.google.android.youtube.intent...
call                -a "com.google.android.youtube.intent.action.U...
Name: com_google_android_youtube_com_google_android_apps_youtube_app_application_Shell_UploadActivity__UPLOAD__DEFAULT__video, dtype: object



#-a / -c /-n / -t will be automatically passed when calling the function
df.com_google_android_youtube_com_google_android_apps_youtube_app_application_Shell_UploadActivity__UPLOAD__DEFAULT__video.call 
Out[20]: 
-a "com.google.android.youtube.intent.action.UPLOAD"
-c "android.intent.category.DEFAULT"
-n "com.google.android.youtube/com.google.android.apps.youtube.app.application.Shell_UploadActivity"
-t "video"
package: com.google.android.youtube/com.google.android.apps.youtube.app.application.Shell_UploadActivity
AutoVerify: false
Type: video
mHasPartialTypes: true
mPriority: 0
Scheme:


# If you want to upload a video on YouTube, for example, you can complete the adb call like this:

df.com_google_android_youtube_com_google_android_apps_youtube_app_application_Shell_UploadActivity__UPLOAD__DEFAULT__video.call('-d file:///storage/emulated/0/DCIM/SharedFolder/xxa.mp4') 

Executing: am start -a "com.google.android.youtube.intent.action.UPLOAD" -c "android.intent.category.DEFAULT" -n "com.google.android.youtube/com.google.android.apps.youtube.app.application.Shell_UploadActivity" -t "video" -d file:///storage/emulated/0/DCIM/SharedFolder/xxa.mp4
b'Starting: Intent { act=com.google.android.youtube.intent.action.UPLOAD cat=[android.intent.category.DEFAULT] dat=file:///storage/emulated/0/DCIM/SharedFolder/xxa.mp4 typ=video cmp=com.google.android.youtube/com.google.android.apps.youtube.app.application.Shell_UploadActivity }\r\n'

# if you pass stop=True / wait=True, the adb command will be executed with -S / -W respectively 


```

