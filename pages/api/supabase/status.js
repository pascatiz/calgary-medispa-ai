import { createClient } from '@supabase/supabase-js';
export default async function handler(req, res) {
  try {
    const supabase = createClient(
      process.env.NEXT_PUBLIC_SUPABASE_URL,
      process.env.SUPABASE_SERVICE_ROLE_KEY
    );
    const { data, error } = await supabase.from('system_config').select('count').limit(1);
    if (error) throw error;
    res.status(200).json({ status: 'connected', timestamp: new Date().toISOString() });
  } catch (error) {
    res.status(500).json({ status: 'error', message: error.message });
  }
}
