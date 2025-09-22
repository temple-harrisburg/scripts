function Get-MediaDuration {
	param (
		[string] $files # the pattern to pass to the Get-ChildItem cmdlet
	)
	# check ffprobe is on path
	if ($null -eq (Get-Command "ffprobe" -ErrorAction SilentlyContinue)) {
		throw [System.Exception]::new("Could not find ffprobe. Install ffmpeg and/or make sure it is on your PATH")
	}
	
	$total = 0;
	$durations = Get-ChildItem -File $files | ForEach-Object { 
		$duration = ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 $_;
		$total += $duration;
		[pscustomobject]@{
			file     = $_.BaseName; 
			duration = '{0:hh\:mm\:ss}' -f ([timespan]::FromSeconds($duration)) 
		} 
	};
	$durations += [pscustomobject]@{file = "Total"; duration = '{0:hh\:mm\:ss}' -f ([timespan]::FromSeconds($total)); }
	return $durations
}
