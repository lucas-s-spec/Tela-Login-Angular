import reflex as rx

TOOLTIP_PROPS = {
    "content_style": {
        "background": "rgba(255, 255, 255, 0.96)",
        "borderColor": "#E5E7EB",
        "borderRadius": "0.75rem",
        "boxShadow": "0 10px 15px -3px rgba(0, 0, 0, 0.1)",
        "fontFamily": "Montserrat, sans-serif",
        "fontSize": "0.875rem",
        "padding": "0.5rem 1rem",
    },
    "item_style": {"color": "#374151", "fontWeight": "500"},
    "label_style": {"color": "#111827", "fontWeight": "600", "marginBottom": "0.25rem"},
    "separator": "",
}


def dark_mode_tooltip_style() -> str:
    return "[&_.recharts-tooltip-wrapper]:!z-[50] [&_.recharts-default-tooltip]:!bg-white dark:[&_.recharts-default-tooltip]:!bg-gray-800 dark:[&_.recharts-default-tooltip]:!border-gray-700 [&_.recharts-tooltip-item]:!text-gray-600 dark:[&_.recharts-tooltip-item]:!text-gray-300 [&_.recharts-tooltip-label]:!text-gray-900 dark:[&_.recharts-tooltip-label]:!text-white"