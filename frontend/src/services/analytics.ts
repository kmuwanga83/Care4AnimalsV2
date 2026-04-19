// frontend/src/services/analytics.ts

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export interface AnalyticsEvent {
  farmer_id?: number;
  event_type: string;
  metadata: Record<string, any>;
}

export const trackEngagement = async (event: AnalyticsEvent) => {
  try {
    const response = await fetch(`${API_URL}/analytics/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        farmer_id: event.farmer_id,
        event_type: event.event_type,
        metadata_json: JSON.stringify(event.metadata),
      }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error("Analytics Tracking Error:", error);
  }
};