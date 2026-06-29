import { useEffect, useState } from "react";

type Reading = {
  temperature: number;
  humidity: number;
  timestamp: string;
};

export default function App() {
  const [data, setData] = useState<Reading | null>(null);

  async function fetchLatest() {
    try {
      const res = await fetch("http://127.0.0.1:8000/latest");
      const json = await res.json();
      setData(json);
    } catch (err) {
      console.error("Failed to fetch:", err);
    }
  }

  useEffect(() => {
    fetchLatest();

    const interval = setInterval(() => {
      fetchLatest();
    }, 3000); // refresh every 3 seconds

    return () => clearInterval(interval);
  }, []);

  if (!data) {
    return <div style={{ padding: 20 }}>Loading...</div>;
  }

  return (
    <div style={{ padding: 20, fontFamily: "Arial" }}>
      <h1>Smart Hygrometer Dashboard</h1>

      <div style={{ marginTop: 20 }}>
        <h2>Current Reading</h2>

        <p>🌡 Temperature: {data.temperature.toFixed(1)} °C</p>
        <p>💧 Humidity: {data.humidity.toFixed(1)} %</p>
        <p>🕒 Time: {data.timestamp}</p>
      </div>
    </div>
  );
}