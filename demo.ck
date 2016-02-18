//---------------------------
// Globals
//---------------------------

// timing
1::minute / 120 => dur beat;

// note range
[0, 2, 3, 5, 7, 9, 10] @=> int scaleTones[];
[3, 6] @=> int octaveRange[];

// patch
Rhodey m => JCRev r => Echo a => dac;

220.0 => m.freq;
0.8 => m.gain;
.8 => r.gain;
.2 => r.mix;
1000::ms => a.max;
250::ms => a.delay;
.10 => a.mix;

//---------------------------
// Note changer
//---------------------------

// continually changing note
Math.random2(octaveRange[0], octaveRange[1]) * 12 => int note;

// converts an integer to a midi note
(octaveRange[1] - octaveRange[0]) * scaleTones.cap() => int max;
fun int itom(int i) {
    // range handling
    if (i > max) {
        max => i;
    } else if (i < 0) {
        0 => i;
    }
    
    // find octav base
    Math.floor(i / scaleTones.cap()) $ int + octaveRange[0] => int octave;
    // find scale tone
    scaleTones[i % scaleTones.cap()] => int tone;
    
    // combine values
    return octave * 12 + tone;
}

fun void changeNote() {
    // fluctuate i
    Math.random2(-2, 2) +=> note;
    if (note > max)
        max => note;
    else if (note < 0)
        0 => note;
    
    // convert i to note
    Std.mtof(itom(note)) => m.freq;
    
    // play
    1 => m.noteOn;
}

// initialize moog freq
Std.mtof(itom(note)) => m.freq;

//---------------------------
// OSC rhythm input
//---------------------------

// set up osc receiver
OscRecv recv;
6449 => recv.port;
recv.listen();
recv.event("/demo/rhythm/subdiv,i") @=> OscEvent msg_received;

// continually receive messages
while (msg_received => now) {
	while (msg_received.nextMsg() != 0) {
		msg_received.getInt() => int subDiv;
		<<< subDiv >>>;
		
		for (0 => int j; j < subDiv; j++) {
			changeNote();
			beat / subDiv => now;
		}
	}
}