class Dashboard {
    constructor() {
        this.eventsContainer = document.getElementById('events-container');
        this.pollInterval = 15000; // 15 seconds
        this.init();
    }

    init() {
        this.loadEvents();
        this.startPolling();
    }

    async loadEvents() {
        try {
            const response = await fetch('/api/events');
            const events = await response.json();

            if (events.length > 0) {
                this.displayEvents(events);
            } else {
                this.displayNoEvents();
            }
        } catch (error) {
            console.error('Error loading events:', error);
            this.displayError();
        }
    }

    displayEvents(events) {
        this.eventsContainer.innerHTML = '';

        events.forEach(event => {
            const eventElement = this.createEventElement(event);
            this.eventsContainer.appendChild(eventElement);
        });
    }

    createEventElement(event) {
        const div = document.createElement('div');
        div.className = `event-item ${event.action}`;

        const message = this.formatMessage(event);

        div.innerHTML = `
            <div class="event-message">${message}</div>
            <div class="event-meta">ID: ${event.request_id} | ${event.action}</div>
        `;

        return div;
    }

    formatMessage(event) {
        const author = event.author;
        const timestamp = this.formatTimestamp(event.timestamp);

        if (event.action === 'push') {
            return `"${author}" pushed to "${event.to_branch}" on ${timestamp}`;
        } else if (event.action === 'pull_request') {
            return `"${author}" submitted a pull request from "${event.from_branch}" to "${event.to_branch}" on ${timestamp}`;
        } else if (event.action === 'merge') {
            return `"${author}" merged branch "${event.from_branch}" to "${event.to_branch}" on ${timestamp}`;
        }

        return `"${author}" performed ${event.action} on ${timestamp}`;
    }

    formatTimestamp(timestamp) {
        const date = new Date(timestamp);
        const options = {
            day: 'numeric',
            month: 'long',
            year: 'numeric',
            hour: 'numeric',
            minute: '2-digit',
            hour12: true,
            timeZoneName: 'short'
        };
        return date.toLocaleString('en-US', options);
    }

    displayNoEvents() {
        this.eventsContainer.innerHTML = `
            <div class="no-events">
                <p>No events yet. Configure your GitHub webhook to start receiving events.</p>
            </div>
        `;
    }

    displayError() {
        this.eventsContainer.innerHTML = `
            <div class="no-events">
                <p>Error loading events. Please try again.</p>
            </div>
        `;
    }

    startPolling() {
        setInterval(() => {
            this.loadEvents();
        }, this.pollInterval);
    }
}

// Initialize dashboard when page loads
document.addEventListener('DOMContentLoaded', () => {
    new Dashboard();
});