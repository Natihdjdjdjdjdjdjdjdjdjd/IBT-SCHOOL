'use strict';


// PART 1: FUNCTION BASICS
//s ==========================================

// Sum any number of distances
const sumDistances = (...distances) => {
    return distances.reduce((total, distance) => total + distance, 0);
};

// Calculate base fare
// Default rate = 15 ETB per kilometer
const calculateBaseFare = (totalDistance, ratePerKm = 15) => {
    return totalDistance * ratePerKm;
};

// Format currency
const formatCurrency = (amount) => {
    return `${amount.toFixed(2)} ETB`;
};


// ==========================================
// PART 2: HIGHER-ORDER FUNCTIONS
// ==========================================

// Create a surge pricing function
function makeSurgeMultiplier(surgeRate) {
    return (baseFare) => {
        return baseFare * surgeRate;
    };
}


// ==========================================
// PART 3: CLOSURES
// ==========================================

// Track driver's completed trips privately
function makeDriverTracker() {
    let tripsCompleted = 0;

    return {
        recordTrip: () => {
            tripsCompleted++;
        },

        getTrips: () => {
            return tripsCompleted;
        }
    };
}


// ==========================================
// PART 4: COMPOSITION & CALLBACKS
// ==========================================

function generateReceipt(distances, surgeFn, tracker, callback) {

    // 1. Record the trip
    tracker.recordTrip();

    // 2. Calculate total distance
    const totalDistance = sumDistances(...distances);

    // 3. Calculate base fare
    const baseFare = calculateBaseFare(totalDistance);

    // 4. Apply surge pricing
    const totalFare = surgeFn(baseFare);

    // 5. Format fare
    const formattedFare = formatCurrency(totalFare);

    // 6. Create receipt
    const message =
        `Trip #${tracker.getTrips()}: Total Fare is ${formattedFare}.`;

    // 7. Call callback
    callback(message);
}


// ==========================================
// TESTING
// ==========================================

// Create driver tracker
const tayesTracker = makeDriverTracker();

// Create pricing functions
const standardPricing = makeSurgeMultiplier(1.0);
const rushHourPricing = makeSurgeMultiplier(1.5);

// Callback
const printToConsole = (message) => console.log(message);

// Ride 1
generateReceipt(
    [2, 3],
    standardPricing,
    tayesTracker,
    printToConsole
);

// Ride 2
generateReceipt(
    [10],
    rushHourPricing,
    tayesTracker,
    printToConsole
);