<script>
	import * as data from '../../../../outputs/flat.json';
	import { getSexagenaryCycle } from '../util/year';

	const Records = data.default;
	const yearsRecorded = Object.keys(Records)
		.map((year) => Number(year))
		.sort((a, b) => a - b);

	const years = yearsRecorded;

	let viewPoint = 0;
	$: viewYear = yearsRecorded[viewPoint];
	$: viewEvent = Records[viewYear.toString()];

	$: eventPlain = viewEvent.event.plain;
	$: records = viewEvent.records;
	$: volume = viewEvent.volume;
	$: record = viewEvent.record;

	let pane;

	const handleWheel = (e) => {
		const { deltaY } = e;

		if (deltaY > 0) {
			if (viewPoint == years.length - 1) return;

			viewPoint += 1;
		} else {
			if (viewPoint == 0) return;
			viewPoint -= 1;
		}

		if (e.cancelable) {
			e.preventDefault();
		}
	};
</script>

<svelte:window on:wheel={handleWheel} />

<div class="h-full flex flex-col">
	<div class="w-svw overflow-x-hidden" bind:this={pane}>
		<div
			class="flex flex-row ease-out transition-all duration-1000 pt-5"
			style="transform:translateX({-viewPoint * 200}px)"
		>
			{#each years as year, index}
				<div
					class="text-slate-50 w-[200px] shrink-0 font-serif justify-center flex flex-col gap-5 items-center"
				>
					<p
						class="text-lg ease-out transition-all duration-500"
						style="opacity:{viewPoint === index ? '80%' : '20%'};"
					>
						{getSexagenaryCycle(year).vn}
					</p>
					<p
						class="text-xl ease-out transition-all duration-500"
						style="transform:scale({viewPoint === index ? '2.5' : '1'})"
					>
						{year > 0 ? `${year} AD` : `${-year} BC`}
					</p>
					<p
						class="text-lg ease-out transition-all duration-500"
						style="opacity:{viewPoint === index ? '80%' : '20%'};"
					>
						{getSexagenaryCycle(year).cn}
					</p>
				</div>
			{/each}
		</div>
	</div>
	<dir></dir>
	<div class="text-white mt-10 max-w-[1000px]">{eventPlain}</div>
</div>
