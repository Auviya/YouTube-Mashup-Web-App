#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import multiprocessing
from pytube import YouTube
import threading
import os
import sys
from moviepy.editor import VideoFileClip,AudioFileClip
from pydub import AudioSegment
from moviepy.editor import VideoFileClip
import shutil


# In[38]:

# urls=[
#   'https://www.youtube.com/watch?v=6DdAzVDVBpw',
#   'https://www.youtube.com/watch?v=h8DLofLM7No',
#   'https://www.youtube.com/watch?v=8xg3vE8Ie_E',
#   'https://www.youtube.com/watch?v=IdneKLhsWOQ'
# ]
# n=2
# t=50
urls=sys.argv[1].split(',')
t=int(sys.argv[2])
n=int(sys.argv[3])
# print(urls)
# print("t"+str(t))
# print("n"+str(n))
if(os.path.isdir('downloads')):
    shutil.rmtree('downloads')
if(os.path.isfile('final.mp3')):
    os.remove('final.mp3')
if(os.path.isfile('results.zip')):
    os.remove('results.zip')
os.mkdir('downloads')



# In[39]:




numberOfCores = multiprocessing.cpu_count()
print ("Num of cores are: ", numberOfCores)


# In[40]:




activeThread = threading.activeCount()
print ("Num of threads: ",activeThread)


# In[41]:
def sort(urls,t,n):
    i=0
    vlen=[]
    for u in urls:
        try:
            yt = YouTube(u);
            video_length = yt.length
            vlen.append(video_length)
            # Print the video length
            print("Video length",i," :", video_length, "seconds") 
            i=i+1
        except:
            continue

    df=(pd.DataFrame({'u':urls,'v':vlen}).sort_values(by="v"))
    return(df[df['v']>=t]['u'])




def downloading(urls,t,n):
    i=0
    # print(i)
    for u in urls:
        # print(i)
        try:
            yt = YouTube(u);
            mp4_files = yt.streams.filter(file_extension="mp4");
            video= mp4_files.get_by_resolution("360p");
            path=video.download();
            os.rename(path,os.getcwd()+'/downloads/vid'+str(i)+'.mp4');
            # The path of the source video
            src_file = 'downloads/vid'+str(i)+'.mp4'
            # The path of the destination video
            dst_file = 'downloads/tvid'+str(i)+'.mp4'
            #Load the video using VideoFileClip
            video = VideoFileClip(src_file)
            # Trim the video from second 0 to second 10
            trimmed_video = video.subclip(0, t)
            # Save the trimmed video
            trimmed_video.write_videofile(dst_file)
            mp4_file ="downloads/tvid"+str(i)+'.mp4'#video file name
            mp3_file="downloads/aud"+str(i)+'.mp3'#create new audio file
            videoclip = VideoFileClip(mp4_file)
            audioclip = videoclip.audio
            audioclip.write_audiofile(mp3_file)
            audioclip.close()
            videoclip.close()
            i=i+1;
            if(i==n):
                return
        except:
            if(os.path.isfile('/downloads/vid'+str(i)+'.mp4')):
                os.remove('/downloads/vid'+str(i)+'.mp4')
            if(os.path.isfile('/downloads/tvid'+str(i)+'.mp4')):
                os.remove('/downloads/tvid'+str(i)+'.mp4')
            if(os.path.isfile('/downloads/aud'+str(i)+'.mp4')):
                os.remove('/downloads/aud'+str(i)+'.mp4')
            continue
        
        


# In[42]:



# In[43]:


# def vidtoaud(n):
#     for i in range(0,n):
#         mp4_file ="tvid"+str(i)+'.mp4'#video file name
#         mp3_file="aud"+str(i)+'.mp3'#create new audio file
#         videoclip = VideoFileClip(mp4_file)
#         audioclip = videoclip.audio
#         audioclip.write_audiofile(mp3_file)
#         audioclip.close()
#         videoclip.close()
    


# In[44]:


# vidtoaud(len(urls))


# In[45]:


# def trimming(n):
#     for i in range(0,n):
#         audio = AudioSegment.from_file("aud"+str(i)+".mp3", format="mp3")
#         start_time =0 # 30 seconds
#         end_time = 30 * 1000 # 60 seconds
#         cut_audio = audio[start_time:end_time]
#         cut_audio.export("output"+str(i)+".mp3", format="mp3")
                


# In[46]:


# trimming(len(urls))


# In[47]:


from pydub import AudioSegment
def merge(n):
    
    aud = AudioSegment.from_file("downloads/aud0.mp3", format="mp3")
    for i in range(1,n):
        aud1=AudioSegment.from_file("downloads/aud"+str(i)+".mp3", format="mp3")
        aud=aud+aud1
    aud.export('final.mp3',format="mp3")


# In[48]:


print("DOWNLOADING")
nurls=sort(urls,t,n)
downloading(nurls,t,n)
print("######MERGING")
merge(n)
shutil.rmtree('downloads')

# In[ ]:





# In[ ]:





# In[13]:





# In[14]:





# In[15]:





# In[ ]:





# In[ ]:





# In[ ]:





 


# In[ ]:





# In[ ]:





# In[ ]:




