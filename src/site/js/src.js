(()=>{
const d=document,now=new Date();
const meses=['jan','fev','mar','abr','mai','jun','jul','ago','set','out','nov','dez'];
const m=d.querySelector('[data-mes]');if(m)m.textContent=meses[now.getMonth()]+'/'+now.getFullYear();
const a=d.querySelector('[data-ano]');if(a)a.textContent=now.getFullYear();

// dias até o próximo dia 20
const dd=d.querySelector('[data-dias]');
if(dd){const t=new Date(now.getFullYear(),now.getMonth(),20);const today=new Date(now.getFullYear(),now.getMonth(),now.getDate());
 if(today>t)t.setMonth(t.getMonth()+1);const n=Math.round((t-today)/864e5);dd.dataset.n=n;dd.textContent=n;}

// header
const top=d.getElementById('top');
const dock=d.querySelector('.dock');const onS=()=>{top.classList.toggle('is-s',scrollY>24);dock&&dock.classList.toggle('on',scrollY>520)};onS();addEventListener('scroll',onS,{passive:true});

const reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;

// ficha: ticks em sequência
const ficha=d.querySelector('.ficha');
const runFicha=()=>{const li=ficha.querySelectorAll('li');li.forEach((l,i)=>setTimeout(()=>{l.classList.add('on');if(i===li.length-1)ficha.classList.add('done')},reduce?0:600+i*420))};

// contador
const count=el=>{const n=+el.dataset.n;if(reduce||!n){return}const t0=performance.now(),dur=1100;const f=t=>{const p=Math.min(1,(t-t0)/dur);el.textContent=Math.round(n*(1-Math.pow(1-p,3)));if(p<1)requestAnimationFrame(f)};el.textContent=0;requestAnimationFrame(f)};

if(!('IntersectionObserver' in window)){d.querySelectorAll('.rv').forEach(e=>e.classList.add('in'));runFicha();return}
const io=new IntersectionObserver(es=>{es.forEach(e=>{if(!e.isIntersecting)return;const el=e.target;
  const sib=[...el.parentElement.children].filter(c=>c.classList.contains('rv'));const i=Math.max(0,sib.indexOf(el));
  el.style.transitionDelay=Math.min(i,6)*80+'ms';el.classList.add('in');io.unobserve(el);
  if(el.classList.contains('hero__visual'))runFicha();
  if(el.querySelector&&el.querySelector('[data-dias]'))count(dd);
  if(el.classList.contains('tl__i')&&el.classList.contains('is-now'))el.parentElement.style.setProperty('--p','12.5%');
})},{rootMargin:'0px 0px -8% 0px',threshold:.12});
d.querySelectorAll('.rv').forEach(e=>io.observe(e));
})();
