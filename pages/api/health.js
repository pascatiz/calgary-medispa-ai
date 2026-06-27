// pages/api/health.js
// PeterOS Calgary MediSpa AI - Health Check Endpoint
export default async function handler(req, res) {
  const health = {
    status: 'healthy',
    service: 'PeterOS Calgary MediSpa AI',
    version: '1.0.0',
    timestamp: new Date().toISOString(),
    environment: process.env.NODE_ENV || 'production',
    checks: {
      api: 'ok',
      supabase: process.env.NEXT_PUBLIC_SUPABASE_URL ? 'configured' : 'missing',
      telegram: process.env.TELEGRAM_BOT_TOKEN ? 'configured' : 'missing',
      openai: process.env.OPENAI_API_KEY ? 'configured' : 'missing',
      anthropic: process.env.ANTHROPIC_API_KEY ? 'configured' : 'missing',
    },
    uptime: process.uptime ? process.uptime() : null,
  };
  const allConfigured = Object.values(health.checks).every(v => v === 'ok' || v === 'configured');
  res.status(allConfigured ? 200 : 206).json(health);
}
