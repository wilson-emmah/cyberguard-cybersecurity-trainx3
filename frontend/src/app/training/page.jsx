'use client';
import{useEffect,useState}from'react';import Link from'next/link';import{api}from'../../lib/api';
export default function Training(){
 const[sess,setSess]=useState(null),[active,setActive]=useState(null),[result,setResult]=useState(null),[nextScenario,setNextScenario]=useState(null),[e,setE]=useState(''),[loading,setLoading]=useState(true);
 async function load(){try{let x=await api('/sessions/active/');if(!x)x=await api('/sessions/start/',{method:'POST',body:'{}'});setSess(x);setActive(x.current_scenario)}catch(x){setE(x.message)}finally{setLoading(false)}}
 useEffect(()=>{load()},[]);
 async function answer(i){try{
   const r=await api(`/scenarios/${active.id}/submit/`,{method:'POST',body:JSON.stringify({choice:i})});
   setResult(r);
   const nextIndex=(sess.current_index||0)+1;
   const saved=await api(`/sessions/${sess.id}/save/`,{method:'POST',body:JSON.stringify({answered_id:active.id,current_index:nextIndex,score:(sess.score||0)+r.points_awarded})});
   setSess(saved);setNextScenario(saved.current_scenario);
 }catch(x){setE(x.message)}}
 async function restart(){setResult(null);setLoading(true);try{const x=await api('/sessions/start/',{method:'POST',body:JSON.stringify({restart:true})});setSess(x);setActive(x.current_scenario)}catch(x){setE(x.message)}finally{setLoading(false)}}
 if(loading)return <main className="container page"><div className="card">Loading your training session…</div></main>;
 if(active)return <><nav className="nav"><Link className="logo" href="/">Cyber<span>Guard</span></Link><div className="links"><Link href="/dashboard">Dashboard</Link><Link href="/ai-coach">AI Coach</Link></div></nav><main className="container page">
   <div className="progressWrap"><div><strong>Training progress</strong><span>{sess.progress}%</span></div><div className="progress"><i style={{width:`${sess.progress}%`}}/></div></div>
   <div className="card" style={{marginTop:20}}><p className="eyebrow">{active.scenario_type} · Level {active.difficulty}</p><h1>{active.title}</h1><p>{active.description}</p><pre className="scenario">{active.prompt}</pre>
   {!result?active.choices.map((x,i)=><button className="choice" key={i} onClick={()=>answer(i)}>{String.fromCharCode(65+i)}. {x}</button>):
   <div className={result.correct?'success':'error'}><h2>{result.correct?'✓ Correct!':'✗ Not quite'}</h2><p><strong>+{result.points_awarded} XP</strong></p><p>{result.explanation}</p><div className="links"><button className="button" onClick={()=>{setResult(null);setActive(nextScenario)}}>Next Scenario</button><Link className="button outline" href="/ai-coach">Ask AI Coach</Link></div></div>}
   {e&&<p className="error">{e}</p>}</div>
 </main></>;
 return <main className="container page"><div className="card"><p className="eyebrow">TRAINING COMPLETE</p><h1>Excellent work.</h1><p>You completed this training session with <strong>{sess?.score||0} XP</strong>.</p><div className="links"><button className="button" onClick={restart}>Start Again</button><Link className="button outline" href="/risk">View Risk Profile</Link></div></div></main>
}