export default {
  async fetch(request, env) {
    try {
      const obj = await env.BUCKET.get('vectors.json');
      if (!obj) return new Response('no object');
      const text = await obj.text();
      const data = JSON.parse(text);
      return new Response('vectors: ' + data.length);
    } catch (e) {
      return new Response('error: ' + e.message);
    }
  }
};
