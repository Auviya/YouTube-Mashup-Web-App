const express=require('express');
const path=require('path');
const axios=require('axios');
const fs = require('fs');
const {spawn} = require('child_process');
const ytdl = require('ytdl-core');
var nodemailer=require("nodemailer");
const JSZip = require('jszip');
const zip = new JSZip();
const app=express();
const port=process.env.PORT || 3000;
app.set('view engine','ejs');
app.set('views',path.join(__dirname,'/views'));

app.use(express.urlencoded({extended:true}));
app.use(express.static(path.join(__dirname,'/public')))
app.get('/mashup',(req,res)=>{
    console.log("request!");
    res.render('home')
})
app.post('/mashup',async function(req,res){
    console.log("POST REQUEST!!")
    const {artist,vidqt,time,email}=req.body;
    //console.log(artist);
    //console.log(vidqt);
    

    //GETTING URLs
    const url=`https://youtube.googleapis.com/youtube/v3/search?part=snippet&type=video&videoDuration=short&maxResults=${vidqt*2}&q=${artist} songs&key=AIzaSyDnDhzGaA9eB1sgg_hQjL0KgueCMnK0_Ww`;
    const resp=await axios.get(url)
    const urls=[]
    for(let v of resp.data.items)
    {
        urls.push(`https://www.youtube.com/watch?v=${v.id.videoId}`)
    }
    // const urls=[
    //     'https://www.youtube.com/watch?v=SmaY7RfBgas',
    //     'https://www.youtube.com/watch?v=PJWemSzExXs',
    //     'https://www.youtube.com/watch?v=vA86QFrXoho',
    //     'https://www.youtube.com/watch?v=zx0YGEi32r0',
    //     'https://www.youtube.com/watch?v=XtCQOmyA0a0',
    //     'https://www.youtube.com/watch?v=9et5qzuzbQM',
    //     'https://www.youtube.com/watch?v=0P3Gt-60yLc',
    //     'https://www.youtube.com/watch?v=GHcyIh5V3TM',
    //     'https://www.youtube.com/watch?v=hUORvCLETbI',
    //     'https://www.youtube.com/watch?v=J3m3uptDf0Q'
    //   ]


    console.log(urls)
    console.log(time)
    let dataToSend='';
    const python = spawn('python', ['yt2.py',urls,time,vidqt]);
    python.stdout.on('data', function (data) {
        console.log(data.toString());
    });
    python.on('close', (code) => {
       console.log(`child process close all stdio with code ${code}`);
       if(code!=0){
        //    res.send("Oops there was an error please try again")
        res.render('oops')
       }else{
           //We have succefully made the file now lets
           //zip it and send it
           try {
                const data = fs.readFileSync('final.mp3');
                zip.file("final.mp3", data);
            
                zip.generateNodeStream({ type: 'nodebuffer', streamFiles: true })
                    .pipe(fs.createWriteStream('results.zip'))
                    .on('finish', function () {
                        console.log("results.zip written.");
                    });
            } catch (err) {
                console.log("error in zipping")
                console.error(err)
                res.render('oops')
            }
            var transporter=nodemailer.createTransport({
                service:'gmail',
                auth:{
                    user:'your gmail email',
                    pass:'your app password'
                }
            });
            var mailOptions={
                from:'auviya023@gmail.com',
                to:email,
                subject:'Here is your mashup',
                html:'<h1>Thanks for using our webapp.</h1><p>Here is your mashup</p>',
                attachments:[
                    {
                        filename:'results.zip',
                        path:'results.zip'
            
                    }
                ]
            };
            transporter.sendMail(mailOptions,function(err,info){
                if(err){
                    console.log(err);
                    //res.send("Error in mailing")
                    res.render('oops')
                }else{
                    console.log("Email sent"+info.response);
                    //res.send("We have sent you a mail!")
                    res.render('exit')
                }
            });
            
        

       }
       
    })
    


    
    //DOWNLOADING VIDEOS
})
app.listen(port,()=>{
    console.log("Listening now");
})




// async function downloading(urls){
//     let i=0
//     for(let u of urls){
//         await download(u,i);
//         i=i+1;
//         console.log(`done downloading ${i}`);
//     }
// }

// function download(url,i){

//     return new Promise(function(resolve,reject){
//         console.log(`downloading ${i}`);
//         let ystream=ytdl(url,{format:'mp4'})
//         ystream.pipe(fs.createWriteStream(`video${i}.mp4`));     
//         ystream.on('end',function(data){
//             resolve();
//         })
//     })
// }
