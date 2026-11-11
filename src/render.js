const {chromium}=require('playwright');const fs=require('fs');const path=require('path');
const SITE=process.argv[2];const B=__dirname,O=B+'/dist';
const emb=fs.readFileSync(B+'/logo_gold.svg','utf8');
const f=n=>'file://'+B+'/site/fonts/'+n;
const css=`@font-face{font-family:P;src:url(${f('playfair-display-latin-wght-italic.woff2')});font-style:italic;font-weight:400 900}
@font-face{font-family:P;src:url(${f('playfair-display-latin-wght-normal.woff2')});font-weight:400 900}
@font-face{font-family:M;src:url(${f('manrope-latin-wght-normal.woff2')});font-weight:200 800}
*{margin:0;box-sizing:border-box}body{width:1200px;height:630px;background:#0F0E0C;color:#EEE7D9;font-family:M;position:relative;overflow:hidden}
.r{position:absolute;inset:0;background:repeating-linear-gradient(180deg,transparent 0 47px,rgba(201,168,106,.07) 47px 48px)}
.g{position:absolute;width:900px;height:900px;right:-250px;top:-260px;background:radial-gradient(closest-side,rgba(201,168,106,.16),transparent)}
.e{position:absolute;right:80px;top:70px;width:370px;height:493px}.e svg{width:100%;height:100%}
.t{position:absolute;left:80px;top:78px;width:700px}
.k{font-weight:700;font-size:18px;letter-spacing:.18em;text-transform:uppercase;color:#C9A86A;display:flex;align-items:center;gap:14px}.k:before{content:"";width:34px;height:8px;border-radius:4px;background:#C9A86A}
h1{font-family:P;font-weight:500;font-size:84px;line-height:1;letter-spacing:-.02em;margin-top:34px}h1 em{color:#C9A86A}
.b{position:absolute;left:80px;bottom:70px;display:flex;align-items:baseline;gap:22px}
.b b{font-family:P;font-style:italic;font-weight:700;font-size:40px;color:#C9A86A}.b span{font-size:20px;color:#ABA293}`;
(async()=>{const b=await chromium.launch();
const p=await b.newPage({viewport:{width:1200,height:630}});
await p.setContent(`<style>${css}</style><div class=r></div><div class=g></div><div class=e>${emb}</div><div class=t><div class=k>Bragança Paulista · SP</div><h1>Seus números <em>em ordem.</em><br>Sua empresa <em>em frente.</em></h1></div><div class=b><b>Contábil Couto</b><span>MEI · Simples · Presumido · Real</span></div>`);
await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(200);
await p.screenshot({path:O+'/img/og.jpg',type:'jpeg',quality:86});
const ic=fs.readFileSync(O+'/icon.svg','utf8');
for(const s of [32,180,192,512]){const q=await b.newPage({viewport:{width:s,height:s}});await q.setContent(`<style>*{margin:0}svg{width:${s}px;height:${s}px;display:block}</style>`+ic);
 await q.screenshot({path:O+(s==180?'/apple-touch-icon.png':s==32?'/fav32.png':`/icon-${s}.png`),omitBackground:true});await q.close();}
const l=await b.newPage({viewport:{width:600,height:600}});await l.setContent(`<style>*{margin:0}body{width:600px;height:600px;background:#0F0E0C;display:grid;place-items:center}svg{width:330px;height:440px}</style>`+emb);
await l.screenshot({path:O+'/img/logo.png'});await b.close();})();
