import { NextRequest } from 'next/server';

export async function POST(req: NextRequest) {
  const { scenario } = await req.json();

  // Proxy the request to your FastAPI backend
  const backendResponse = await fetch('http://localhost:8000/analyze-stream', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ scenario }),
  });

  // Stream the response back to the client
  return new Response(backendResponse.body, {
    headers: { 'Content-Type': 'text/plain' },
  });
}
