import { useState, useEffect } from 'react'

function App() {
    const [pos,setPos] = useState(null)
    const [data,setData] = useState(null)
    const [loading,setLoading] = useState(false)

    useEffect(()=>{
        if(!navigator.geolocation) return
        navigator.geolocation.getCurrentPosition(s=>{
            setPos({lat: s.coords.latitude, lon: s.coords.longitude})
        }, console.error)
    },[])

    async function fetchPlan(){
        if(!pos) return
        setLoading(true)
        const resp = await fetch(`${import.meta.env.VITE_API_BASE || 'http://localhost:8000'}/data`,{
            method:'POST',
            headers:{'Content-Type':'application/json'},
            body: JSON.stringify({lat:pos.lat, lon:pos.lon, city: null})
        })
        const j = await resp.json()
        setData(j)
        setLoading(false)
    }

    return (
    <div style={{padding:20,fontFamily:'system-ui, sans-serif'}}>
        <h1>DayMate</h1>
        <p>Personalized planning powered by weather + local news.</p>
        <button onClick={fetchPlan} disabled={!pos || loading}>{loading? "Planning...":"Get today's plan"}</button>
        {data && (
            <div style={{marginTop:20}}>
                <h2>Plan</h2>
                <pre style={{whiteSpace:'pre-wrap'}}>{JSON.stringify(data.plan, null, 2)}</pre>
                <h3>Weather (current)</h3>
                <pre>{JSON.stringify(data.weather.current, null, 2)}</pre>
                <h3>Top news</h3>
                <ul>{data.news.map((a,i)=>(<li key={i}><a href={a.url} target='_blank'>{a.title}</a></li>))}</ul>
            </div>
        )}
    </div>
    )
}
export default App