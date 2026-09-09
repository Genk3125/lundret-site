import os, subprocess, html, json, textwrap, urllib.parse
from pathlib import Path
import requests
import imageio_ffmpeg
from faster_whisper import WhisperModel

OUT=Path('dist'); OUT.mkdir(exist_ok=True)
video=OUT/'source.mp4'
ffmpeg=imageio_ffmpeg.get_ffmpeg_exe()

# Transcribe spoken English with timestamps.
model=WhisperModel('small.en', device='cpu', compute_type='int8')
segments,_=model.transcribe(str(video), vad_filter=True, beam_size=3)
segments=list(segments)

def translate(s):
    try:
        r=requests.get('https://translate.googleapis.com/translate_a/single',params={'client':'gtx','sl':'en','tl':'ja','dt':'t','q':s},timeout=20)
        r.raise_for_status()
        return ''.join(x[0] for x in r.json()[0] if x and x[0]).strip()
    except Exception:
        return s

def ts(sec):
    ms=max(0,int(round(sec*1000))); h=ms//3600000; ms%=3600000; m=ms//60000; ms%=60000; s=ms//1000; ms%=1000
    return f'{h:02}:{m:02}:{s:02},{ms:03}'

srt=[]
for i,seg in enumerate(segments,1):
    en=seg.text.strip()
    if not en: continue
    ja=translate(en)
    srt += [str(i), f'{ts(seg.start)} --> {ts(seg.end)}', ja, '']
Path('ja.srt').write_text('\n'.join(srt), encoding='utf-8')
Path('transcript.json').write_text(json.dumps([{'start':s.start,'end':s.end,'en':s.text.strip(),'ja':translate(s.text.strip())} for s in segments if s.text.strip()],ensure_ascii=False,indent=2),encoding='utf-8')

# Japanese font
font=Path('NotoSansJP.ttf')
if not font.exists():
    urls=[
      'https://raw.githubusercontent.com/notofonts/noto-cjk/main/Sans/Variable/TTF/Subset/NotoSansJP-VF.ttf',
      'https://github.com/google/fonts/raw/main/ofl/notosansjp/NotoSansJP%5Bwght%5D.ttf'
    ]
    for u in urls:
        try:
            rr=requests.get(u,timeout=30); rr.raise_for_status(); font.write_bytes(rr.content); break
        except Exception: pass

# Mask the original lower-third English captions and burn Japanese subtitles.
style="FontName=Noto Sans JP,FontSize=22,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,BorderStyle=1,Outline=3,Shadow=0,Alignment=2,MarginV=40"
vf=f"drawbox=x=0:y=ih*0.76:w=iw:h=ih*0.24:color=black@0.82:t=fill,subtitles=ja.srt:fontsdir=.:force_style='{style}'"
cmd=[ffmpeg,'-y','-i',str(video),'-vf',vf,'-c:v','libx264','-preset','veryfast','-crf','19','-c:a','aac','-b:a','192k','-movflags','+faststart',str(OUT/'video-ja.mp4')]
subprocess.run(cmd,check=True)
print('DONE', OUT/'video-ja.mp4', (OUT/'video-ja.mp4').stat().st_size)
