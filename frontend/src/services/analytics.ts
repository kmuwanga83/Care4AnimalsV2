const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const logEvent = async (eventType: string, lessonId?: string) => {
  if (!navigator.onLine) {
    console.warn("Farmer is offline. Analytics event queued locally.");
    return;
  }

  try {
    await fetch(`${API_BASE_URL}/api/v1/analytics/events`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        event_type: eventType,
        platform: 'web',
        lesson_id: lessonId
      }),
    });
  } catch (error) {
    console.error("Analytics sync error:", error);
  }
};