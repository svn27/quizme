from youtube_transcript_api import YouTubeTranscriptApi


def get_transcript_from_link(yt_link:str):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(get_video_code_from_link(yt_link))

        transcript_text = ""

        for line in transcript:
            transcript_text += line['text']

        return transcript_text

    except:
        return "Error"

def get_video_code_from_link(video_link:str):
    video_id = ""
    
    for i in range(len(video_link) - 1, -1, -1):
        if video_link[i] != '=':
            video_id += video_link[i]
        else:
            break

    return video_id[::-1]