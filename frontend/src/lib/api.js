export const API=process.env.NEXT_PUBLIC_API_URL||'http://localhost:8000/api';
export const getToken=()=>typeof window==='undefined'?null:localStorage.getItem('access_token');
export const saveTokens=d=>{localStorage.setItem('access_token',d.access);localStorage.setItem('refresh_token',d.refresh||'')};
export const logout=()=>{localStorage.removeItem('access_token');localStorage.removeItem('refresh_token')};
export async function api(path,options={}){const token=getToken();const headers={'Content-Type':'application/json',...(options.headers||{})};if(token)headers.Authorization=`Bearer ${token}`;const r=await fetch(`${API}${path}`,{...options,headers,cache:'no-store'});let d=null;try{d=await r.json()}catch{}if(!r.ok)throw new Error(d?.detail||Object.values(d||{}).flat().join(' ')||'Request failed');return d}
