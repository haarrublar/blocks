import say from 'say';

/**
 * @param {string} text - The text to speak
 * @param {string} voice - Optional: 'Alex', 'Samantha', 'Daniel'
 */
export function botVoice(text, voice = 'Samantha') {
    return new Promise((resolve, reject) => {
        console.log(`Bot speaking: "${text}"`);
        
        say.speak(text, voice, 0.8, (err) => {
            if (err) {
                console.error("Speech Error:", err);
                reject(err);
            } else {
                resolve();
            }
        });
    });
}

