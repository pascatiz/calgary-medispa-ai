export default function Home() {
  return (
    <div style={{padding:'2rem',fontFamily:'sans-serif',background:'#0a0a0a',minHeight:'100vh',color:'#fff'}}>
      <h1>PeterOS Calgary MediSpa AI</h1>
      <p>Cloud-based AI automation command centre</p>
      <ul>
        <li><a href="/api/health" style={{color:'#4ade80'}}>Health Check</a></li>
        <li><a href="/api/supabase/status" style={{color:'#4ade80'}}>Supabase Status</a></li>
      </ul>
    </div>
  );
}
